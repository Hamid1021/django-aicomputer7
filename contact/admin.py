from django.contrib import admin
from .models import ContactMessage, Request

# ---------------- ContactMessage Admin ----------------


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read",
                    "date_create", "date_update")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-date_create",)
    actions = ["mark_as_read"]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(
            request, f"{updated} پیام علامت‌گذاری شد به عنوان خوانده شده.")
    mark_as_read.short_description = "علامت‌گذاری پیام‌ها به عنوان خوانده شده"


# ---------------- Request Admin ----------------
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson_title", "teacher_name",
                    "is_active", "is_deleted", "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("user__username", "lesson_title",
                     "teacher_name", "description")
    ordering = ("-date_create",)
