from django.db import models


class FileLibrary(models.Model):
    title = models.CharField(
        "عنوان فایل", max_length=200, null=True, blank=True)
    file = models.FileField("فایل", upload_to="library_files/")
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "فایل"
        verbose_name_plural = "کتابخانه فایل‌ها"
        ordering = ["-date_create"]

    def __str__(self):
        return self.title if self.title else self.file.name
