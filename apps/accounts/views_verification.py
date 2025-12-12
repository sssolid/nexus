"""
Updated views for accounts with email verification workflow.
Replace the existing UserRegistrationView in apps/accounts/views.py
"""
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView

from .forms import UserRegistrationForm
from .models_verification import EmailVerification, PendingApproval
from .security import enforce_2fa
from .tasks import (
    send_admin_notification_email,
    send_approval_confirmation_email,
    send_verification_email,
)

User = get_user_model()


class UserRegistrationView(CreateView):
    """
    View for customer registration with email verification.
    """
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:verification_sent')
    
    def form_valid(self, form):
        """
        Save the user and trigger email verification process.
        User account is created but not active until approved.
        """
        # Set user as inactive until approved
        form.instance.is_active = False
        form.instance.email_verified = False
        form.instance.is_approved = False
        
        # Save user
        response = super().form_valid(form)
        user = self.object
        
        # Create email verification token
        email_verification = EmailVerification.create_for_user(user)
        
        # Send verification email asynchronously
        transaction.on_commit(
            lambda: send_verification_email.delay(user.id, email_verification.token)
        )
        
        return response


def verify_email_view(request, token):
    """
    Handle email verification link clicks.
    """
    # Find verification record
    verification = get_object_or_404(EmailVerification, token=token)
    
    # Check if already verified
    if verification.email_verified:
        messages.info(request, 'Your email has already been verified.')
        return redirect('two_factor:login')
    
    # Check if expired
    if verification.is_expired:
        messages.error(
            request,
            format_html(
                'This verification link has expired. '
                '<a href="{}">Request a new verification email</a>.',
                reverse('accounts:resend_verification')
            )
        )
        return redirect('two_factor:login')
    
    # Mark as verified
    verification.mark_verified()
    
    # Create pending approval record
    PendingApproval.objects.get_or_create(user=verification.user)
    
    # Notify sales team
    send_admin_notification_email.delay(verification.user.id)
    
    messages.success(
        request,
        'Your email has been verified! Your registration is now pending approval by our team.'
    )
    
    return redirect('accounts:verification_success')


def verification_sent_view(request):
    """
    View shown after registration form submission.
    """
    return render(request, 'accounts/verification_sent.html')


def verification_success_view(request):
    """
    View shown after successful email verification.
    """
    return render(request, 'accounts/verification_success.html')


def resend_verification_view(request):
    """
    Allow users to request a new verification email.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email, email_verified=False)
            
            # Create new verification token
            email_verification = EmailVerification.create_for_user(user)
            
            # Send verification email
            send_verification_email.delay(user.id, email_verification.token)
            
            messages.success(
                request,
                'A new verification email has been sent to your email address.'
            )
            return redirect('accounts:verification_sent')
            
        except User.DoesNotExist:
            # Don't reveal if email exists in database
            messages.success(
                request,
                'If an unverified account exists with this email, '
                'a new verification link has been sent.'
            )
            return redirect('accounts:verification_sent')
    
    return render(request, 'accounts/resend_verification.html')


@login_required
@enforce_2fa
@user_passes_test(lambda u: u.is_staff or (u.is_employee and u.employee_role == User.EmployeeRole.SALES))
def approve_registration_view(request, user_id):
    """
    Allow sales reps to approve registrations and assign customer numbers.
    """
    pending_approval = get_object_or_404(
        PendingApproval,
        user_id=user_id,
        status=PendingApproval.ApprovalStatus.PENDING,
    )

    if request.method == 'POST':
        customer_number = request.POST.get('customer_number')
        notes = request.POST.get('notes', '')

        if not customer_number:
            messages.error(request, 'Customer number is required.')
            return redirect('accounts:approve_registration', user_id=user_id)

        # Approve the registration
        pending_approval.approve(
            reviewed_by=request.user,
            customer_number=customer_number,
            notes=notes,
        )

        # Send approval confirmation email
        send_approval_confirmation_email.delay(pending_approval.user.id)

        messages.success(
            request,
            f'Registration approved for {pending_approval.user.email}',
        )

        return redirect('accounts:pending_approvals_list')

    return render(request, 'accounts/approve_user.html', {
        'approval': pending_approval,          # what template expects
        'user': pending_approval.user,         # what template expects
    })


@login_required
@enforce_2fa
@user_passes_test(lambda u: u.is_staff or u.is_employee and u.employee_role == User.EmployeeRole.SALES)
def reject_registration_view(request, user_id):
    """
    Allow sales reps to reject registrations.
    """
    pending_approval = get_object_or_404(
        PendingApproval,
        user_id=user_id,
        status=PendingApproval.ApprovalStatus.PENDING
    )
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        
        # Reject the registration
        pending_approval.reject(
            reviewed_by=request.user,
            notes=notes
        )
        
        # Send rejection notification email (optional)
        # send_rejection_notification_email.delay(pending_approval.user.id, notes)
        
        messages.success(
            request,
            f'Registration rejected for {pending_approval.user.email}'
        )
        
        return redirect('accounts:pending_approvals_list')
    
    return render(request, 'accounts/reject_user.html', {
        'approval': pending_approval,          # what template expects
        'user': pending_approval.user,         # what template expects
    })


@login_required
@enforce_2fa
@user_passes_test(lambda u: u.is_staff or u.is_employee and u.employee_role == User.EmployeeRole.SALES)
def pending_approvals_list_view(request):
    """
    List all pending registrations for sales team review.
    """
    pending_approval = PendingApproval.objects.filter(
        status=PendingApproval.ApprovalStatus.PENDING
    ).select_related('user').order_by('-created_at')
    
    return render(request, 'accounts/pending_approvals_index.html', {
        'pending_approval': pending_approval,
    })
