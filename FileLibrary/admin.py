from django.contrib import admin
from .models import FileLibrary


@admin.register(FileLibrary)
class FileLibraryAdmin(admin.ModelAdmin):
    list_display = ("title", "file_preview", "is_active",
                    "is_deleted", "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("title", "file")
    ordering = ("-date_create",)

    readonly_fields = ("file_preview",)

    def file_preview(self, obj):
        if obj.file:
            if obj.file.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                return f'<img src="{obj.file.url}" style="height: 50px;" />'
            return obj.file.name
        return "-"
    file_preview.short_description = "پیش‌نمایش فایل"
    file_preview.allow_tags = True
