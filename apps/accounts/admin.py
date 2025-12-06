"""
Admin configuration for the accounts application.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomerPricingTier, User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = [
        'email', 'full_name', 'user_type', 'employee_role',
        'is_active', 'is_verified', 'is_approved', 'created_at'
    ]
    list_filter = [
        'user_type', 'employee_role', 'is_active',
        'is_verified', 'is_approved', 'is_staff'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'customer_number', 'company_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        (_('User Type'), {
            'fields': ('user_type', 'employee_role', 'employee_id')
        }),
        (_('Customer Info'), {
            'fields': ('customer_number', 'company_name'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_verified', 'is_approved',
                'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'last_login_ip')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'user_type',
                'first_name', 'last_name', 'is_active'
            ),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    
    list_display = [
        'user', 'city', 'state', 'country',
        'notifications_enabled', 'default_export_format'
    ]
    list_filter = [
        'notifications_enabled', 'email_notifications',
        'newsletter_subscription', 'country'
    ]
    search_fields = ['user__email', 'city', 'state', 'postal_code']
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Address'), {
            'fields': (
                'address_line1', 'address_line2',
                'city', 'state', 'postal_code', 'country'
            )
        }),
        (_('Notifications'), {
            'fields': (
                'notifications_enabled', 'email_notifications',
                'newsletter_subscription'
            )
        }),
        (_('Preferences'), {
            'fields': ('items_per_page', 'default_export_format')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomerPricingTier)
class CustomerPricingTierAdmin(admin.ModelAdmin):
    """Admin interface for CustomerPricingTier model."""
    
    list_display = [
        'user', 'tier', 'effective_date',
        'expiration_date', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'tier', 'effective_date']
    search_fields = ['user__email', 'user__customer_number', 'tier__name']
    date_hierarchy = 'effective_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'tier', 'is_active')
        }),
        (_('Dates'), {
            'fields': ('effective_date', 'expiration_date')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        """Set created_by field when creating new instance."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
