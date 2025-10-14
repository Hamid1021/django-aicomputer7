from django.db import models
from account.models import USER as User


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'ارسال شد'),
        ('failed', 'ناموفق'),
        ('pending', 'در صف'),
    ]

    subject = models.CharField("موضوع ایمیل", max_length=250)
    to_email = models.EmailField("گیرنده")
    from_email = models.EmailField("فرستنده", null=True, blank=True)
    message = models.TextField("متن ایمیل")
    status = models.CharField(
        "وضعیت ارسال", max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField("پیام خطا", null=True, blank=True)
    created_by = models.ForeignKey(
        User, verbose_name="ارسال‌کننده", on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "لاگ ایمیل"
        verbose_name_plural = "لاگ ایمیل‌ها"
        ordering = ["-date_create"]

    def __str__(self):
        return f"{self.subject} → {self.to_email} ({self.status})"
