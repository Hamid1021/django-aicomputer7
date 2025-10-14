from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid
from django.apps import apps
from django.contrib.auth.hashers import make_password
from random import randint
from django.utils import timezone
from club.models import Club
from extensions.utils import jalali_converter, get_filename_ext


def generate_ranint():
    return "".join([str(randint(0, 9)) for _ in range(4)])


def upload_to_Image_file(instance, filename):
    name, ext = get_filename_ext(filename)
    return f"users/images/{instance.username}/{instance.username}{ext}"


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # str(uuid.uuid4())[-1:8:-1] is a 24 random character
        extra_fields.setdefault('custom_user_id', str(uuid.uuid4())[:11:-1])
        extra_fields.setdefault('gender', "m")
        extra_fields.setdefault('pass_per_save', password or "")
        extra_fields.setdefault('code_send', generate_ranint())
        extra_fields.setdefault('email_sended', False)
        return self._create_user(username, email, password, **extra_fields)

    def _create_super_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('pass_per_save', password or "")
        extra_fields.setdefault('custom_user_id', str(uuid.uuid4())[:11:-1])
        extra_fields.setdefault('gender', "m")
        extra_fields.setdefault('code_send', generate_ranint())
        extra_fields.setdefault('email_sended', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_super_user(username, email, password, **extra_fields)


class UserSide(models.Model):
    u_title = models.CharField("عنوان سمت کاربر", max_length=150)
    description = models.TextField("توضیح", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_deleted = models.BooleanField("حذف شده", default=False)
    date_create = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    date_update = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "سمت کاربر"
        verbose_name_plural = "سمت‌های کاربران"
        ordering = ["u_title"]

    def __str__(self):
        return self.u_title


class USER(AbstractUser):
    pass_per_save = models.CharField(
        verbose_name="گذر واژه هش نشده", max_length=255, blank=True
    )
    GENDER_CHOICES = (
        ("m", "مرد"),
        ("w", "زن"),
        ("b", "ترجیح می دهم نگویم"),
    )
    gender = models.CharField(
        verbose_name="جنسیت", max_length=1, null=False,
        blank=False, choices=GENDER_CHOICES, default="m"
    )
    avatar = models.ImageField(
        verbose_name="آواتار", upload_to=upload_to_Image_file, null=True,
        blank=True, default="None"
    )
    phone_number = models.CharField(
        verbose_name="شماره همراه", max_length=11, null=True, blank=True, unique=True
    )
    custom_user_id = models.CharField(
        verbose_name="کد اختصاصی کاربر", max_length=24, null=True, blank=True, unique=True
    )
    code_send = models.IntegerField(
        verbose_name="کد ارسال شده", null=True, blank=True
    )
    email_sended = models.BooleanField(
        default=False, verbose_name="ایمیل ارسال شده است"
    )
    meli_code = models.CharField(
        verbose_name="کد ملی", max_length=10, null=True, blank=True, unique=True
    )
    uni_code = models.CharField(
        verbose_name="کد دانشجویی", max_length=24, null=True, blank=True, unique=True
    )
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="انجمن")
    user_side = models.ForeignKey(UserSide, verbose_name="سمت کاربر", on_delete=models.CASCADE, null=True, blank=True,)
    objects = CustomUserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.first_name != "" or self.last_name != "":
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        else:
            full_name = '%s' % (self.username, )
            return full_name.strip()
