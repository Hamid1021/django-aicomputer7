from .models import Request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, "پیام شما با موفقیت ارسال شد 🌟")
            return redirect("contact")
        else:
            messages.error(request, "لطفاً همه فیلدها را پر کنید ❗")

    return render(request, "contact.html")


@login_required
def request_view(request):
    user_requests = Request.objects.filter(user=request.user, is_deleted=False)[:5]

    if request.method == "POST":
        title = request.POST.get("lesson_title")
        teacher = request.POST.get("teacher_name")
        desc = request.POST.get("description")

        if title:
            Request.objects.create(
                user=request.user,
                lesson_title=title,
                teacher_name=teacher,
                description=desc,
            )
            messages.success(request, "درخواست شما ثبت شد ✅")
            return redirect("request")
        else:
            messages.error(request, "عنوان درخواست الزامی است ❗")

    context = {"user_requests": user_requests}
    return render(request, "request.html", context)
