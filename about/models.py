from django.db import models

# Create your models here.


class FAQ(models.Model):
    question = models.CharField("سوال", max_length=300)
    answer = models.TextField("پاسخ", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"
        ordering = ["-date_create"]

    def __str__(self):
        return self.question


class TeamMember(models.Model):
    full_name = models.CharField("نام و نام خانوادگی", max_length=150)
    position = models.CharField("سمت / نقش", max_length=100)
    bio = models.TextField("بیوگرافی", null=True, blank=True)
    photo = models.ImageField(
        "عکس", upload_to="team_photos/", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class AboutPage(models.Model):
    PAGE_TYPE_CHOICES = [
        ('history', 'تاریخچه'),
        ('mission', 'ماموریت'),
        ('team', 'تیم'),
        ('faq', 'سوالات متداول'),
        ('other', 'سایر'),
    ]

    title = models.CharField("عنوان صفحه", max_length=200)
    slug = models.SlugField("نامک", max_length=200, unique=True)
    page_type = models.CharField(
        "نوع صفحه", max_length=20, choices=PAGE_TYPE_CHOICES, default='other')
    content = models.TextField("محتوا", null=True, blank=True)
    image = models.ImageField(
        "تصویر", upload_to="about_pages/", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "صفحه درباره"
        verbose_name_plural = "صفحات درباره"
        ordering = ["-date_create"]

    def __str__(self):
        return self.title
