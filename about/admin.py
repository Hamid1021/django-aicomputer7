from django.contrib import admin
from .models import AboutPage, TeamMember, FAQ

# ---------------- AboutPage Admin ----------------


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("title", "page_type", "is_active",
                    "is_deleted", "date_create", "date_update")
    list_filter = ("page_type", "is_active", "is_deleted")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date_create",)

# ---------------- TeamMember Admin ----------------


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "is_active",
                    "is_deleted", "date_create", "date_update")
    list_filter = ("position", "is_active", "is_deleted")
    search_fields = ("full_name", "bio")
    ordering = ("full_name",)

# ---------------- FAQ Admin ----------------


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "is_deleted",
                    "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("question", "answer")
    ordering = ("-date_create",)
