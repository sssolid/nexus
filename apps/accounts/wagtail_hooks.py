"""
Wagtail hooks for accounts app.
Adds pending approvals menu item to Wagtail admin.
"""
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from apps.accounts.models import User
from apps.accounts.models_verification import PendingApproval


@hooks.register('register_admin_menu_item')
def register_pending_approvals_menu():
    """
    Add 'Pending Approvals' menu item to Wagtail admin sidebar.
    Only visible to sales reps and admins.
    """
    return MenuItem(
        'Pending Approvals',
        reverse('pending_approvals:index'),
        icon_name='user',
        order=300  # Adjust order as needed
    )


@hooks.register('construct_main_menu')
def hide_menu_from_non_sales(request, menu_items):
    """
    Hide pending approvals menu from users who aren't sales reps or admins.
    """
    if not request.user.is_authenticated:
        return
    
    # Only show to sales reps and admins
    if not (request.user.is_employee and 
            request.user.employee_role in [User.EmployeeRole.SALES, User.EmployeeRole.ADMIN]):
        menu_items[:] = [
            item for item in menu_items 
            if item.name != 'pending-approvals'
        ]


@hooks.register('construct_homepage_panels')
def add_pending_approvals_panel(request, panels):
    """
    Add pending approvals summary panel to Wagtail admin homepage.
    Only for sales reps and admins.
    """
    if not request.user.is_authenticated:
        return
    
    if not (request.user.is_employee and 
            request.user.employee_role in [User.EmployeeRole.SALES, User.EmployeeRole.ADMIN]):
        return
    
    # Count pending approvals
    pending_count = PendingApproval.objects.filter(
        status=PendingApproval.ApprovalStatus.PENDING
    ).count()
    
    if pending_count > 0:
        from wagtail.admin.ui.components import Component
        
        class PendingApprovalsPanel(Component):
            """Summary panel for pending approvals."""
            
            def render_html(self, parent_context):
                return f"""
                <section class="panel summary nice-padding">
                    <h2 class="visuallyhidden">Pending User Approvals</h2>
                    <div class="panel-header">
                        <div class="summary-single">
                            <a href="{reverse('pending_approvals:index')}">
                                <div class="icon icon-warning"></div>
                                <h3>{pending_count}</h3>
                                <p>Pending Approval{'s' if pending_count != 1 else ''}</p>
                            </a>
                        </div>
                    </div>
                </section>
                """
        
        panels.append(PendingApprovalsPanel())
