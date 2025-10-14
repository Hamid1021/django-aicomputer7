from django.db import models
from django.urls import reverse
from account.models import USER as User
from club.models import Club
from extensions.utils import jalali_converter
from django_ckeditor_5.fields import CKEditor5Field


# ---------------- EventsCategory ----------------


class EventsCategory(models.Model):
    title = models.CharField("عنوان دسته‌بندی", max_length=150)
    description = models.TextField("توضیحات", null=True, blank=True)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    event_bg_color = models.CharField(
        "رنگ پس‌زمینه", max_length=7, null=True, blank=True)

    class Meta:
        verbose_name = "دسته‌بندی رویداد"
        verbose_name_plural = "دسته‌بندی‌های رویداد"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("events:events_by_category", kwargs={ "pk": self.pk})

    def __str__(self):
        return self.title


# ---------------- Event ----------------
class Event(models.Model):
    SAVE_TYPE_CHOICES = [
        ('P', 'منتشر شده'),
        ('N', 'منتشر نشده'),
    ]

    ACCESS_TYPE_CHOICES = [
        ('web', 'آنلاین'),
        ('location', 'حضوری'),
    ]

    title = models.CharField("عنوان رویداد", max_length=250)
    slug = models.SlugField("نامک", max_length=250, unique=True)
    event_cat = models.ManyToManyField(
        EventsCategory, verbose_name="دسته‌بندی‌ها")
    teacher_name = models.CharField(
        "نام استاد", max_length=150, null=True, blank=True)
    price = models.DecimalField(
        "قیمت", max_digits=10, decimal_places=2, null=True, blank=True)
    capacity = models.PositiveIntegerField("ظرفیت", null=True, blank=True)
    access_type = models.CharField(
        "نوع دسترسی", max_length=10, choices=ACCESS_TYPE_CHOICES, default='web')
    access_type_address = models.CharField(
        "آدرس/لینک دسترسی", max_length=300, null=True, blank=True)
    event_start_time = models.DateTimeField(
        "شروع رویداد", null=True, blank=True)
    event_end_time = models.DateTimeField(
        "پایان رویداد", null=True, blank=True)
    short_describe = CKEditor5Field(
        "توضیح کوتاه", max_length=300, null=True, blank=True)
    full_describ = CKEditor5Field("توضیح کامل", null=True, blank=True)
    club = models.ForeignKey(Club, verbose_name="انجمن",
                             on_delete=models.SET_NULL, null=True, blank=True)
    important_info = models.TextField("اطلاعات مهم", null=True, blank=True)
    event_image = models.ImageField(
        "تصویر رویداد", upload_to="event_images/", null=True, blank=True)
    save_type = models.CharField(
        "وضعیت انتشار", max_length=1, choices=SAVE_TYPE_CHOICES, default='N')
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"
        ordering = ["-date_create"]

    def get_absolute_url(self):
        return reverse("events:event", kwargs={"slug": self.slug, "pk": self.pk})

    def jevent_start_time(self):
        return jalali_converter(self.event_start_time)

    def __str__(self):
        return self.title


# ---------------- EventUser ----------------
class EventUser(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)
    club = models.ForeignKey(Club, verbose_name="کلاب",
                             on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, verbose_name="رویداد", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "شرکت‌کننده رویداد"
        verbose_name_plural = "شرکت‌کنندگان رویداد"

    def __str__(self):
        return f"{self.user} - {self.event}"
