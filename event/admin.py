from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from django.contrib import admin
from .models import Event, EventsCategory, EventUser
from django.utils.html import format_html
from django.contrib import admin
from colorfield.widgets import ColorWidget

# ---------------- EventsCategory Admin ----------------


class EventsCategoryForm(forms.ModelForm):
    class Meta:
        model = EventsCategory
        fields = "__all__"
        widgets = {
            "event_bg_color": ColorWidget(attrs={"type": "color"})
        }


@admin.register(EventsCategory)
class EventsCategoryAdmin(admin.ModelAdmin):
    form = EventsCategoryForm
    list_display = ("title", "is_active", "is_deleted", "colored_event_bg",
                    "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("title", "description")
    ordering = ("title",)

    def colored_event_bg(self, obj):
        return format_html(
            '<div style="width: 50px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.event_bg_color
        )
    colored_event_bg.short_description = "رنگ پس‌زمینه"


# ---------------- EventUser Inline ----------------
class EventUserInline(admin.TabularInline):
    model = EventUser
    extra = 1
    fk_name = "event"
    fields = ("user", "club")
    autocomplete_fields = ("user", "club")


# ---------------- Event Admin ----------------


class EventAdminForm(forms.ModelForm):
    short_describe = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"), label="توضیح مختصر")
    full_describ = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"), label="متن رویداد")

    class Meta:
        model = Event
        fields = "__all__"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ("title", "author", "access_type", "save_type",
                    "is_active", "is_deleted", "date_create", "date_update")
    list_filter = ("access_type", "save_type", "is_active",
                   "is_deleted", "event_cat", "club")
    search_fields = ("title", "short_describe", "full_describ", "teacher_name")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date_create",)
    filter_horizontal = ("event_cat",)
    inlines = [EventUserInline]


# ---------------- EventUser Admin ----------------
@admin.register(EventUser)
class EventUserAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "club")
    list_filter = ("event", "club")
    search_fields = ("user__username", "event__title", "club__club_name")
    ordering = ("user",)
