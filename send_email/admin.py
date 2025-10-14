from django.contrib import admin
from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("subject", "to_email", "from_email",
                    "status", "created_by", "date_create")
    list_filter = ("status", "created_by", "date_create")
    search_fields = ("subject", "to_email", "from_email",
                     "message", "error_message")
    readonly_fields = ("subject", "to_email", "from_email", "message",
                       "status", "error_message", "created_by", "date_create", "date_update")
    ordering = ("-date_create",)
