from django.contrib import admin
from .models import Club
from django.utils.html import format_html
from colorfield.widgets import ColorWidget
from django import forms


class ClubAdminForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = "__all__"
        widgets = {
            "club_color": ColorWidget(attrs={"type": "color"})
        }


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    form = ClubAdminForm
    list_display = ("club_name", "slug", "colored_club_bg", "is_active",
                    "is_deleted", "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("club_name", "slug")
    prepopulated_fields = {"slug": ("club_name",)}
    ordering = ("-date_create",)

    def colored_club_bg(self, obj):
        return format_html(
            '<div style="width: 50px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.club_color
        )
    colored_club_bg.short_description = "رنگ پس‌زمینه"