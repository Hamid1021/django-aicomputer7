from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from django.contrib import admin
from .models import Blog, PostCategory, Tag, Comment, Fav, Save
from django.utils.html import format_html
from django.contrib import admin

from colorfield.widgets import ColorWidget


class EventsCategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = "__all__"
        widgets = {
            "post_bg_color": ColorWidget(attrs={"type": "color"})
        }


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    form = EventsCategoryForm
    list_display = ("title", "colored_post_bg", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("title",)
    ordering = ("title",)

    def colored_post_bg(self, obj):
        return format_html(
            '<div style="width: 50px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.post_bg_color
        )
    colored_post_bg.short_description = "رنگ پس‌زمینه"


# ---------------- Tag Admin ----------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("title",)
    ordering = ("title",)


# ---------------- Comment Inline ----------------


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fk_name = "blog"
    fields = ("user", "message", "is_read", "is_personal", "is_show", "reply")
    readonly_fields = ("date_create",)


class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"))

    class Meta:
        model = Blog
        fields = "__all__"

# ---------------- Blog Admin ----------------


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ("title", "author", "save_type", "is_active",
                    "is_deleted", "date_create", "date_update")
    list_filter = ("save_type", "is_active",
                   "is_deleted", "post_cat", "post_tag")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date_create",)
    # inlines = [CommentInline]
    filter_horizontal = ("post_cat", "post_tag")


# ---------------- Comment Admin ----------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "message", "reply",
                    "is_read", "is_personal", "is_show", "date_create")
    list_filter = ("is_read", "is_personal", "is_show")
    search_fields = ("message", "user__username", "blog__title")
    ordering = ("-date_create",)


# ---------------- Fav Admin ----------------
@admin.register(Fav)
class FavAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "event")
    search_fields = ("user__username",)
    ordering = ("user",)


# ---------------- Save Admin ----------------
@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "event")
    search_fields = ("user__username",)
    ordering = ("user",)
