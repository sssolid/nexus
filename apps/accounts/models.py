"""
User models for the Automotive Catalog System.

Implements a custom user model that supports both customers and employees
with role-based access control.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for User model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
            
        Returns:
            User: The created user instance
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        
        Args:
            email: Superuser's email address
            password: Superuser's password
            **extra_fields: Additional fields for the user model
            
        Returns:
            User: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', User.UserType.EMPLOYEE)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model for the Automotive Catalog System.
    
    Supports both customer and employee user types with role-based permissions.
    Uses email as the primary authentication field instead of username.
    """
    
    class UserType(models.TextChoices):
        """User type choices."""
        CUSTOMER = 'CUSTOMER', _('Customer')
        EMPLOYEE = 'EMPLOYEE', _('Employee')
    
    class EmployeeRole(models.TextChoices):
        """Employee role choices for permission management."""
        ADMIN = 'ADMIN', _('Administrator')
        MANAGER = 'MANAGER', _('Manager')
        SALES = 'SALES', _('Sales Representative')
        SUPPORT = 'SUPPORT', _('Customer Support')
        DATA_ADMIN = 'DATA_ADMIN', _('Data Administrator')
    
    # Remove username field
    username = None
    
    # Primary fields
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
        db_index=True
    )
    
    # Employee-specific fields
    employee_role = models.CharField(
        max_length=20,
        choices=EmployeeRole.choices,
        blank=True,
        null=True,
        db_index=True
    )
    employee_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9-]+$', 'Enter a valid employee ID.')]
    )
    
    # Customer-specific fields
    customer_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        db_index=True
    )
    company_name = models.CharField(max_length=200, blank=True)
    
    # Contact information
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            r'^\+?1?\d{9,15}$',
            'Enter a valid phone number.'
        )]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(
        default=False,
        help_text=_('Designates whether this customer has been approved for access.')
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type', 'is_active']),
            models.Index(fields=['customer_number']),
            models.Index(fields=['employee_id']),
        ]
    
    def __str__(self):
        """String representation of the user."""
        return self.email
    
    @property
    def is_customer(self):
        """Check if user is a customer."""
        return self.user_type == self.UserType.CUSTOMER
    
    @property
    def is_employee(self):
        """Check if user is an employee."""
        return self.user_type == self.UserType.EMPLOYEE
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def has_employee_role(self, role):
        """
        Check if user has a specific employee role.
        
        Args:
            role: Employee role to check
            
        Returns:
            bool: True if user has the role, False otherwise
        """
        return self.is_employee and self.employee_role == role


class UserProfile(models.Model):
    """
    Extended user profile for additional user information and preferences.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    
    # Preferences
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=False)
    
    # UI Preferences
    items_per_page = models.IntegerField(default=50)
    default_export_format = models.CharField(
        max_length=10,
        default='CSV',
        choices=[
            ('CSV', 'CSV'),
            ('EXCEL', 'Excel'),
            ('JSON', 'JSON'),
            ('XML', 'XML'),
        ]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        """String representation of the profile."""
        return f"Profile for {self.user.email}"


class CustomerPricingTier(models.Model):
    """
    Pricing tier assignment for customers.
    Links customers to their specific pricing tiers.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.CUSTOMER},
        related_name='pricing_tiers'
    )
    tier = models.ForeignKey(
        'pricing.PricingTier',
        on_delete=models.CASCADE,
        related_name='customer_assignments'
    )
    effective_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_pricing_assignments'
    )
    
    class Meta:
        verbose_name = _('customer pricing tier')
        verbose_name_plural = _('customer pricing tiers')
        ordering = ['-effective_date']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['effective_date', 'expiration_date']),
        ]
    
    def __str__(self):
        """String representation of the pricing tier assignment."""
        return f"{self.user.email} - {self.tier.name}"
