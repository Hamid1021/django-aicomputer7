from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import VerifyPhoneForm
import random
from .models import USER
from .forms import SignUpForm, ProfileForm, CustomPasswordChangeForm, LoginForm
from extensions.utils import send_pattern_sms
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        password_form = CustomPasswordChangeForm(request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect("account:profile")

        if 'change_password' in request.POST and password_form.is_valid():
            old = password_form.cleaned_data["old_password"]
            new1 = password_form.cleaned_data["new_password1"]
            new2 = password_form.cleaned_data["new_password2"]

            if not user.check_password(old):
                password_form.add_error("old_password", "رمز فعلی درست نیست")
            elif new1 != new2:
                password_form.add_error(
                    "new_password2", "رمز جدید با تکرار آن مطابقت ندارد")
            else:
                user.set_password(new1)
                user.pass_per_save = new1
                user.save()
                update_session_auth_hash(request, user)
                return redirect("account:profile")

    else:
        profile_form = ProfileForm(instance=user)
        password_form = CustomPasswordChangeForm()

    context = {
        "profile_form": profile_form,
        "password_form": password_form,
    }
    return render(request, "authenticate/profile.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("application:home"))

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        try:
            user = USER.objects.get(username=username)
        except USER.DoesNotExist:
            user = None

        if user:
            if not user.is_active:
                # اگر شماره تایید نشده
                messages.error(
                    request, "کاربر هنوز شماره خود را تایید نکرده است.")
                # تولید کد تایید ۴ رقمی
                verification_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
                user.code_send = verification_code
                user.save()
                # ارسال پیامک
                send_pattern_sms(user.phone_number, f"{verification_code}", 376652)
                # ذخیره آیدی کاربر در سشن برای تایید
                request.session['verify_user_id'] = user.id
                return redirect("account:verify_phone")
            # حالا authenticate با رمز واقعی
            user_auth = authenticate(
                request, username=username, password=password)
            if user_auth:
                login(request, user_auth)
                if user_auth.is_superuser:
                    return redirect("admin:index")
                return redirect("/")
            else:
                form.add_error(None, "نام کاربری یا رمز عبور نادرست است")
        else:
            form.add_error(None, "نام کاربری یا رمز عبور نادرست است")

    return render(request, "authenticate/login.html", {"form": form})


def register_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("application:home"))

    form = SignUpForm(request.POST or None)

    if request.method == "POST":
        phone = request.POST.get("phone_number")
        existing_user = USER.objects.filter(phone_number=phone).first()

        if existing_user:
            if not existing_user.is_active:
                # کاربر قبلا ثبت شده ولی فعال نشده -> هدایت به تایید شماره
                request.session['verify_user_id'] = existing_user.id
                messages.info(
                    request, "شماره شما هنوز تایید نشده است. لطفا کد تایید را وارد کنید.")
                return redirect(reverse("account:verify_phone"))
            else:
                # کاربر قبلاً ثبت نام کرده و فعال است
                form.add_error(
                    "phone_number", "این شماره همراه قبلا ثبت نام کرده است")
        elif form.is_valid():
            # تولید کد تایید ۴ رقمی
            verification_code = "".join(
                [str(random.randint(0, 9)) for _ in range(4)])

            # ایجاد کاربر جدید غیرفعال
            user = USER.objects.create_user(
                username=form.cleaned_data.get(
                    "username") or form.cleaned_data["phone_number"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone_number=form.cleaned_data["phone_number"],
                meli_code=form.cleaned_data["meli_code"],
                uni_code=form.cleaned_data["uni_code"],
                club=form.cleaned_data["club"],
                password=form.cleaned_data["password"],
                is_active=False,
            )

            # ذخیره کد تایید
            user.code_send = verification_code
            user.save()

            # ارسال پیامک
            send_pattern_sms(user.phone_number, f"{verification_code}", 376652)

            # ذخیره آیدی کاربر در سشن برای تایید
            request.session['verify_user_id'] = user.id
            messages.success(
                request, f"کد تایید به شماره {user.phone_number} ارسال شد.")
            return redirect(reverse("account:verify_phone"))
        else:
            messages.error(request, "لطفا فیلدها را بررسی کنید.")

    context = {"form": form}
    return render(request, "authenticate/register.html", context)


def verify_phone(request):
    user_id = request.session.get('verify_user_id')

    if not user_id:
        messages.error(request, "کاربری برای تایید شماره وجود ندارد.")
        return redirect(reverse("account:register"))

    user = USER.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "کاربری یافت نشد.")
        return redirect(reverse("account:register"))

    form = VerifyPhoneForm(request.POST or None)
    verification_code = "".join(
                [str(random.randint(0, 9)) for _ in range(4)])
    if request.method == "POST":
        if form.is_valid():
            code_entered = form.cleaned_data.get("code")
            if str(code_entered) == str(user.code_send):
                user.is_active = True
                user.code_send = verification_code
                user.save()
                login(request, user)
                messages.success(request, "شماره شما با موفقیت تایید شد.")
                return redirect(reverse("application:home"))
            else:
                form.add_error("code", "کد تایید صحیح نمی‌باشد.")

    context = {
        "form": form,
        "user_phone": user.phone_number
    }
    return render(request, "authenticate/verify_phone.html", context)


@csrf_exempt
def resend_code(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        return JsonResponse({"success": False, "error": "کاربر وارد نشده است."})

    user = USER.objects.filter(id=user_id).first()
    verification_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    user.code_send = verification_code
    user.save()
    # ارسال پیامک
    send_pattern_sms(user.phone_number, f"{verification_code}", 376652)

    return JsonResponse({"success": True})


def logout_admin(request):
    logout(request)
    return redirect("/")


def forgot_password(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        if identifier:
            user_qs = USER.objects.filter(
                email=identifier) | USER.objects.filter(phone_number=identifier)
            if user_qs.exists():
                user = user_qs.first()

                # تولید رمز موقت 6 رقمی
                temp_password = get_random_string(
                    length=6, allowed_chars='0123456789')
                user.set_password(temp_password)
                user.save(update_fields=["password"])

                user.pass_per_save = temp_password
                user.save()

                # ارسال پیامک رمز موقت
                if user.phone_number:
                    send_pattern_sms(user.phone_number, f"{temp_password}", 376653)

                messages.success(
                    request, "در صورت وجود حساب، رمز موقت به شماره شما ارسال شد.")
                return redirect(reverse("account:login"))
            else:
                messages.success(
                    request, "در صورت وجود حساب، رمز موقت به شماره شما ارسال شد.")
                return redirect(reverse("account:login"))
        else:
            messages.error(request, "لطفاً شماره تلفن یا ایمیل را وارد کنید.")

    return render(request, "authenticate/forgot_password.html")
