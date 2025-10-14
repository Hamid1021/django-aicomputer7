from django.db import models

class Club(models.Model):
    club_name = models.CharField("نام انجمن", max_length=150)
    slug = models.SlugField("نامک", max_length=150, unique=True)
    icon = models.ImageField("آیکون", upload_to="club_icons/", null=True, blank=True)
    club_color = models.CharField("رنگ انجمن", max_length=7, default="#000000")
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)

    class Meta:
        verbose_name = "انجمن "
        verbose_name_plural = "انجمن ها"
        ordering = ["-date_create"]

    def __str__(self):
        return self.club_name
