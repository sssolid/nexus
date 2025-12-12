from django.contrib import admin, messages
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice

from .models import User


@admin.action(description="Reset selected users' 2FA devices (SUPERUSERS ONLY)")
def reset_2fa(modeladmin, request, queryset):
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can reset 2FA devices.")
        return

    user_ids = list(queryset.values_list("id", flat=True))
    totp_deleted = TOTPDevice.objects.filter(user_id__in=user_ids).delete()[0]
    static_deleted = StaticDevice.objects.filter(user_id__in=user_ids).delete()[0]

    messages.success(
        request,
        f"2FA reset complete. Removed {totp_deleted} TOTP devices and {static_deleted} static devices."
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "email_verified", "is_approved", "is_active")
    search_fields = ("email", "customer_number", "employee_id")
    actions = [reset_2fa]
