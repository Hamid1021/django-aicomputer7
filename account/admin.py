from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from account.models import USER, UserSide
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


# ---------------- USER Admin ----------------

@admin.register(USER)
class UserAdmin(UserAdmin):
    fieldsets = (
        ("اطلاعات کاربری", {
            'fields': ('username', 'password', ) #'pass_per_save')
        }),
        (_('اطلاعات شخصی'), {
            'fields': ('first_name', 'last_name', 'gender', 'avatar', 'email')
        }),
        ("اطلاعات هویتی و تماس", {
            'fields': (
                'phone_number', 'meli_code', 'uni_code',
                'custom_user_id', 'code_send', 'email_sended'
            )
        }),
        ("وابستگی‌ها و سمت‌ها", {
            'fields': ('club', 'user_side')
        }),
        (_('سطوح دسترسی'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('تاریخ‌های مهم'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    #readonly_fields = ("pass_per_save",)

    add_fieldsets = (
        ("ایجاد کاربر جدید", {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'gender', 'phone_number'),
        }),
    )

    list_display = (
        'username', 'phone_number', 'email', 'first_name', 'last_name',
        'gender', 'club', 'user_side', 'is_active', 'is_superuser'
    )
    list_display_links = ('username', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active',
                   'gender', 'club', 'user_side')
    search_fields = (
        'username', 'first_name', 'last_name', 'email',
        'phone_number', 'meli_code', 'uni_code', 'custom_user_id'
    )
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    # محدودیت دسترسی برای افزودن
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    # محدودیت حذف
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # تنظیم readonly برای کاربران غیر سوپر
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            pass
            #self.readonly_fields = ("pass_per_save",)
        else:
            self.readonly_fields = (
                "username", "custom_user_id", #"pass_per_save",
                "code_send", "email_sended", "is_active",
                "is_staff", "is_superuser", "groups", "user_permissions",
                "last_login", "date_joined",
            )
        return request.user.is_superuser or (obj and obj.id == request.user.id)
    

    def user_change_password(self, request, id, form_url=''):
        """
        ویوی تغییر رمز عبور: در صورت ارسال POST فرم تغییر رمز عبور پردازش می‌شود.
        """
        user_obj = self.get_object(request, id)
        if not self.has_change_permission(request, user_obj):
            raise PermissionDenied
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user_obj, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر یافت.')
                return HttpResponseRedirect("..")
        else:
            form = AdminPasswordChangeForm(user_obj)

        context = {
            'title': 'تغییر رمز عبور: %s' % user_obj.username,
            'form': form,
            'opts': self.model._meta,
            'original': user_obj,
            'form_url': form_url,
        }
        return TemplateResponse(request, "admin/auth/user/change_password.html", context)

    # فیلتر کوئری برای جلوگیری از مشاهده سایر کاربران
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

# ---------------- UserSide Admin ----------------


@admin.register(UserSide)
class UserSideAdmin(admin.ModelAdmin):
    list_display = ("u_title", "is_active", "is_deleted",
                    "date_create", "date_update")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("u_title", "description")
    ordering = ("u_title",)
