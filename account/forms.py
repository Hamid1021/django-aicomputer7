from .models import USER
from django.contrib.auth.forms import PasswordChangeForm
from account.models import USER as User
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from club.models import Club


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input--style-4",
                "id": "username"
            }
        ))
    password = forms.CharField(
        max_length=100,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "input--style-4", "id": "password",
                   "name": "password"}
        ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError(
                "نام کاربری صحیح نمی باشد دوباره امتحان کنید")
        else:
            return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username, pass_per_save=password)
        if not user:
            raise forms.ValidationError(
                "رمز عبور صحیح نمی باشد دوباره امتحان کنید")
        else:
            return password


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "رمز عبور خود را وارد کنید"
            }
        )
    )
    password_confirm = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "رمز عبور را دوباره وارد کنید"
            }
        )
    )
    first_name = forms.CharField(
        label="نام",
        required=True
    )
    last_name = forms.CharField(
        label="نام خانوادگی",
        required=True
    )
    phone_number = forms.CharField(
        label="شماره همراه",
        required=True
    )
    uni_code = forms.CharField(
        label="کد دانشجویی",
        required=True
    )

    club = forms.ModelChoiceField(
        queryset=Club.objects.filter(is_active=True),
        empty_label="انتخاب انجمن",
        label="انجمن",
        widget=forms.Select(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-center"
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "phone_number",
            "meli_code", "uni_code", "club"
        ]
        widgets = {
            # "username": forms.TextInput(attrs={
            #     "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
            #     "placeholder": "نام کاربری خود را وارد کنید"
            # }),
            "first_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "نام"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "نام خانوادگی"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "مثال: 09123456789", "type": "tel"
            }),
            "meli_code": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "کد ملی"
            }),
            "uni_code": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "کد دانشجویی"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition",
                "placeholder": "ایمیل"
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(
                "این شماره همراه قبلا ثبت نام کرده است")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("فردی با این ایمیل ثبت نام کرده است")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "نام کاربری انتخابی موجود است، نام دیگری وارد کنید")
        return username

    def clean_password_confirm(self):
        pw = self.cleaned_data.get("password")
        pw2 = self.cleaned_data.get("password_confirm")
        if pw != pw2:
            raise forms.ValidationError(
                "تکرار رمز عبور صحیح نمی باشد لطفا بررسی نمایید")
        return pw2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = [
            "first_name", "last_name", "gender", "avatar", "club", "user_side"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
            "gender": forms.Select(attrs={"class": "form-input text-center"}),
            "club": forms.Select(attrs={"class": "form-input text-center"}),
            # فقط نمایش، غیرقابل ویرایش
            "user_side": forms.TextInput(attrs={
                "class": "form-input bg-gray-100 cursor-not-allowed",
                "readonly": True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # مقدار پیش‌فرض user_side به صورت رشته
        if self.instance and self.instance.user_side:
            self.fields['user_side'].initial = self.instance.user_side


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="رمز فعلی",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password1 = forms.CharField(
        label="رمز جدید",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password2 = forms.CharField(
        label="تکرار رمز جدید",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )


class VerifyPhoneForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        label="کد تایید",
        widget=forms.TextInput(
            attrs={
                "class": "form-input text-center text-xl tracking-widest",
                "placeholder": "----",
                "autocomplete": "off"
            }
        )
    )
