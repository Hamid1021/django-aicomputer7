from django.db import models
from account.models import USER as User

# ---------------- ContactMessage ----------------


class ContactMessage(models.Model):
    name = models.CharField("نام فرستنده", max_length=150)
    email = models.EmailField("ایمیل فرستنده")
    subject = models.CharField("موضوع", max_length=200)
    message = models.TextField("پیام")
    is_read = models.BooleanField("خوانده شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "پیام تماس با ما"
        verbose_name_plural = "پیام‌های تماس با ما"
        ordering = ["-date_create"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ---------------- Request ----------------
class Request(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)
    lesson_title = models.CharField("عنوان درخواست", max_length=200)
    teacher_name = models.CharField(
        "نام استاد", max_length=150, null=True, blank=True)
    description = models.TextField("توضیحات", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست‌ها"
        ordering = ["-date_create"]

    def __str__(self):
        return f"{self.user} - {self.lesson_title}"
