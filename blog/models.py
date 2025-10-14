from django.db import models
from account.models import USER as User
from event.models import Event
from django.urls import reverse
from club.models import Club

# ---------------- PostCategory ----------------


class PostCategory(models.Model):
    title = models.CharField("عنوان دسته‌بندی", max_length=150)
    post_bg_color = models.CharField(
        "رنگ پس‌زمینه", max_length=7, null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)

    class Meta:
        verbose_name = "دسته‌بندی پست"
        verbose_name_plural = "دسته‌بندی‌های پست"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("blogs:category", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


# ---------------- Tag ----------------
class Tag(models.Model):
    title = models.CharField("عنوان تگ", max_length=100)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ["title"]

    def __str__(self):
        return self.title


# ---------------- Blog ----------------
class BlogManager(models.Manager):
    def get_all_active(self):
        return self.get_queryset().filter(save_type="P", is_active=True, is_deleted=False)


class Blog(models.Model):
    SAVE_TYPE_CHOICES = [
        ('P', 'منتشر شده'),
        ('N', 'منتشر نشده'),
    ]

    title = models.CharField("عنوان مقاله", max_length=250)
    slug = models.SlugField("نامک", max_length=250, unique=True)
    post_cat = models.ManyToManyField(
        PostCategory, verbose_name="دسته‌بندی‌ها")
    post_tag = models.ManyToManyField(Tag, verbose_name="تگ‌ها", blank=True)
    text = models.TextField("متن مقاله", null=True, blank=True)
    post_image = models.ImageField(
        "عکس مقاله", upload_to="blog_images/", null=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.SET_NULL, null=True, blank=True)
    club = models.ForeignKey(Club, verbose_name="انجمن",
                             on_delete=models.SET_NULL, null=True, blank=True)
    save_type = models.CharField(
        "وضعیت انتشار", max_length=1, choices=SAVE_TYPE_CHOICES, default='N')
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)

    objects = BlogManager()

    def toggle_like(self, user):
        """لایک یا آن‌لایک کردن پست توسط کاربر"""
        if user.is_authenticated:
            if user in self.likes.all():
                self.likes.remove(user)
                return False  # یعنی آن‌لایک شد
            else:
                self.likes.add(user)
                return True  # یعنی لایک شد
        return None  # اگر کاربر لاگین نبود
    
    def get_absolute_url(self):
        return reverse("blogs:blog", kwargs={"slug": self.slug, "pk": self.pk})

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-date_create"]

    def __str__(self):
        return self.title


# ---------------- Comment ----------------
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, verbose_name="مقاله",
                             on_delete=models.CASCADE, related_name="blogs_set")
    event = models.ForeignKey(Event, verbose_name="رویداد",
                              on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField("پیام")
    reply = models.ForeignKey("self", verbose_name="پاسخ به",
                              on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    is_read = models.BooleanField("خوانده شده", default=False)
    is_personal = models.BooleanField("خصوصی", default=False)
    is_show = models.BooleanField("نمایش", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ["-date_create"]

    def __str__(self):
        return f"{self.user} - {self.blog}"


# ---------------- Fav ----------------
class Fav(models.Model):
    blog = models.ForeignKey(Blog, verbose_name="مقاله",
                             on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, verbose_name="رویداد",
                              on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"

    def __str__(self):
        return f"{self.user} - Blog: {self.blog} Event: {self.event}"


# ---------------- Save ----------------
class Save(models.Model):
    blog = models.ForeignKey(Blog, verbose_name="مقاله",
                             on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, verbose_name="رویداد",
                              on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ذخیره"
        verbose_name_plural = "ذخیره‌ها"

    def __str__(self):
        return f"{self.user} - Blog: {self.blog} Event: {self.event}"
