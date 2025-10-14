from django.db import models


# Create your models here.
class Panel_Admin_Settings(models.Model):
    color_chose = (
        ("pr", "صورتی"), ("da", "تیره"), ("in", "آبی"),
        ("su", "سبز"), ("wa", "نارنجی"), ("dn", "قرمز"),
    )
    bg_color_Sidebar = models.CharField(
        max_length=2, choices=color_chose, verbose_name="پس زمینه گزینه ها", blank=True)
    Sidenav_color_chose = (
        ("da", "تیره"), ("tr", "به رنگ پس زمینه"), ("wh", "سفید")
    )
    Sidenav_color = models.CharField(
        max_length=2, choices=Sidenav_color_chose, verbose_name="پس زمینه ناوبر", blank=True)
    fixed_navbar = models.BooleanField(default=True, verbose_name="ناوبر چسبیده",)
    night_mode = models.BooleanField(default=False, verbose_name="حالت شب",)

    class Meta:
        verbose_name = "تنظیم"
        verbose_name_plural = "تنظیمات"
        db_table = 'Panel_Admin_Setting'
