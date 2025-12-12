"""
Wagtail admin views for managing pending user approvals.
This provides a dedicated interface for sales reps to review and approve registrations.
"""
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import FieldPanel
from wagtail.admin.views.generic import IndexView
from wagtail.models import Page

from apps.accounts.models import User
from apps.accounts.models_verification import PendingApproval
from apps.accounts.tasks import send_approval_confirmation_email


def is_sales_rep(user):
    """Check if user is a sales rep or admin."""
    return (
        user.is_authenticated and 
        user.is_employee and 
        user.employee_role in [User.EmployeeRole.SALES, User.EmployeeRole.ADMIN]
    )


class PendingApprovalIndexView(IndexView):
    """
    Custom index view for pending approvals in Wagtail admin.
    """
    model = PendingApproval
    page_title = "Pending User Approvals"
    add_item_label = None  # Don't show "Add" button
    template_name = "wagtailadmin/accounts/../../templates/accounts/pending_approvals_index.html"
    index_url_name = "pending_approvals_index"
    default_ordering = "-created_at"
    
    def get_queryset(self):
        """Return only pending approvals."""
        qs = super().get_queryset()
        return qs.filter(status=PendingApproval.ApprovalStatus.PENDING).select_related('user')
    
    @method_decorator(user_passes_test(is_sales_rep))
    def dispatch(self, request, *args, **kwargs):
        """Ensure only sales reps can access."""
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(is_sales_rep)
def approve_user_view(request, approval_id):
    """
    Handle user approval with customer number assignment.
    """
    approval = get_object_or_404(
        PendingApproval,
        pk=approval_id,
        status=PendingApproval.ApprovalStatus.PENDING
    )
    
    if request.method == 'POST':
        customer_number = request.POST.get('customer_number', '').strip()
        notes = request.POST.get('notes', '').strip()
        
        if not customer_number:
            messages.error(request, 'Customer number is required.')
            return redirect('pending_approvals:approve', approval_id=approval_id)
        
        # Check if customer number already exists
        if User.objects.filter(customer_number=customer_number).exclude(id=approval.user.id).exists():
            messages.error(request, f'Customer number {customer_number} is already in use.')
            return redirect('pending_approvals:approve', approval_id=approval_id)
        
        # Approve the registration
        approval.approve(
            reviewed_by=request.user,
            customer_number=customer_number,
            notes=notes
        )
        
        # Send approval confirmation email
        send_approval_confirmation_email.delay(approval.user.id)
        
        messages.success(
            request,
            f'Successfully approved registration for {approval.user.email} with customer number {customer_number}.'
        )
        
        return redirect('pending_approvals:index')
    
    # GET request - show approval form
    context = {
        'approval': approval,
        'user': approval.user,
    }
    
    return render(request, 'wagtailadmin/accounts/../../templates/accounts/approve_user.html', context)


@user_passes_test(is_sales_rep)
def reject_user_view(request, approval_id):
    """
    Handle user rejection.
    """
    approval = get_object_or_404(
        PendingApproval,
        pk=approval_id,
        status=PendingApproval.ApprovalStatus.PENDING
    )
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '').strip()
        
        if not notes:
            messages.error(request, 'Please provide a reason for rejection.')
            return redirect('pending_approvals:reject', approval_id=approval_id)
        
        # Reject the registration
        approval.reject(
            reviewed_by=request.user,
            notes=notes
        )
        
        messages.success(
            request,
            f'Registration for {approval.user.email} has been rejected.'
        )
        
        return redirect('pending_approvals:index')
    
    # GET request - show rejection form
    context = {
        'approval': approval,
        'user': approval.user,
    }
    
    return render(request, 'wagtailadmin/accounts/../../templates/accounts/reject_user.html', context)


@user_passes_test(is_sales_rep)
def view_user_details(request, approval_id):
    """
    View detailed information about a pending approval.
    """
    approval = get_object_or_404(PendingApproval, pk=approval_id)
    
    context = {
        'approval': approval,
        'user': approval.user,
    }
    
    return render(request, 'wagtailadmin/accounts/user_details.html', context)


# URL patterns for Wagtail admin
urlpatterns = [
    path('', PendingApprovalIndexView.as_view(), name='index'),
    path('<int:approval_id>/approve/', approve_user_view, name='approve'),
    path('<int:approval_id>/reject/', reject_user_view, name='reject'),
    path('<int:approval_id>/details/', view_user_details, name='details'),
]
