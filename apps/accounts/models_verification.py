"""
Email verification tracking model.
Add this to apps/accounts/models.py (append to existing file)
"""

from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .tokens import generate_verification_token


class EmailVerification(models.Model):
    """
    Tracks email verification tokens for new user registrations.
    """
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='email_verifications'
    )
    token = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name = _('email verification')
        verbose_name_plural = _('email verifications')
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation."""
        return f"Verification for {self.user.email}"
    
    @property
    def is_expired(self):
        """Check if verification token has expired (24 hours)."""
        expiry_time = self.created_at + timedelta(hours=24)
        return timezone.now() > expiry_time
    
    def mark_verified(self):
        """Mark email as verified."""
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'verified_at'])
        
        # Update user's is_verified status
        self.user.is_verified = True
        self.user.save(update_fields=['is_verified'])
    
    @classmethod
    def create_for_user(cls, user):
        """
        Create a new email verification token for a user.
        
        Args:
            user: User instance
            
        Returns:
            EmailVerification: Created verification instance
        """
        # Invalidate any existing tokens
        cls.objects.filter(user=user, is_verified=False).delete()
        
        # Create new token
        token = generate_verification_token()
        return cls.objects.create(user=user, token=token)


class PendingApproval(models.Model):
    """
    Tracks users pending approval after email verification.
    """
    
    class ApprovalStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending Review')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
    
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='pending_approval'
    )
    status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True
    )
    customer_number = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Assigned customer number from legacy system')
    )
    notes = models.TextField(
        blank=True,
        help_text=_('Internal notes about this registration')
    )
    reviewed_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_approvals',
        help_text=_('Sales rep who reviewed this registration')
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('pending approval')
        verbose_name_plural = _('pending approvals')
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation."""
        return f"{self.user.email} - {self.status}"
    
    def approve(self, reviewed_by, customer_number, notes=''):
        """
        Approve the registration.
        
        Args:
            reviewed_by: User who approved the registration
            customer_number: Customer number to assign
            notes: Optional notes about approval
        """
        self.status = self.ApprovalStatus.APPROVED
        self.customer_number = customer_number
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        self.notes = notes
        self.save()
        
        # Activate user account
        self.user.is_approved = True
        self.user.is_active = True
        self.user.customer_number = customer_number
        self.user.save(update_fields=['is_approved', 'is_active', 'customer_number'])
    
    def reject(self, reviewed_by, notes=''):
        """
        Reject the registration.
        
        Args:
            reviewed_by: User who rejected the registration
            notes: Reason for rejection
        """
        self.status = self.ApprovalStatus.REJECTED
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        self.notes = notes
        self.save()
        
        # Deactivate user account
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
