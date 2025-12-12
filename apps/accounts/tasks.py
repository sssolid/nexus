"""
Celery tasks for account-related email notifications.
"""
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

User = get_user_model()


@shared_task(bind=True, max_retries=3)
def send_verification_email(self, user_id, verification_token):
    """
    Send email verification link to newly registered user.
    
    Args:
        user_id: User's primary key
        verification_token: Verification token
    """
    try:
        user = User.objects.get(pk=user_id)
        
        # Build verification URL
        verification_url = f"{settings.SITE_URL}{reverse('accounts:verify_email', kwargs={'token': verification_token})}"
        
        # Render email templates
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'Crown Data Portal',
            'support_email': settings.SUPPORT_EMAIL,
        }
        
        html_content = render_to_string('accounts/emails/verification_email.html', context)
        text_content = render_to_string('accounts/emails/verification_email.txt', context)
        
        # Create email
        subject = 'Verify Your Email - Crown Data Portal'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return f"Verification email sent to {user.email}"
        
    except User.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_admin_notification_email(self, user_id):
    """
    Notify sales team that a new user needs approval.
    
    Args:
        user_id: User's primary key
    """
    try:
        user = User.objects.get(pk=user_id)
        
        # Get sales team emails
        sales_emails = User.objects.filter(
            user_type=User.UserType.EMPLOYEE,
            employee_role=User.EmployeeRole.SALES,
            is_active=True
        ).values_list('email', flat=True)
        
        # Also send to support/admin emails from settings
        admin_emails = getattr(settings, 'ADMIN_NOTIFICATION_EMAILS', [])
        all_recipients = list(sales_emails) + admin_emails
        
        if not all_recipients:
            return "No recipients found for admin notification"
        
        # Build approval URL (to admin interface)
        approval_url = f"{settings.SITE_URL}/cms/accounts/pendingapproval/"
        
        # Render email templates
        context = {
            'user': user,
            'approval_url': approval_url,
            'site_name': 'Crown Data Portal',
        }
        
        html_content = render_to_string('accounts/emails/admin_notification.html', context)
        text_content = render_to_string('accounts/emails/admin_notification.txt', context)
        
        # Create email
        subject = f'New Registration Pending Approval - {user.company_name or user.full_name}'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=all_recipients
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return f"Admin notification sent to {len(all_recipients)} recipients"
        
    except User.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_approval_confirmation_email(self, user_id):
    """
    Send email to user confirming their account has been approved.
    
    Args:
        user_id: User's primary key
    """
    try:
        user = User.objects.get(pk=user_id)
        
        # Build login URL
        login_url = f"{settings.SITE_URL}{reverse('accounts:login')}"
        
        # Render email templates
        context = {
            'user': user,
            'login_url': login_url,
            'customer_number': user.customer_number,
            'site_name': 'Crown Data Portal',
            'support_email': settings.SUPPORT_EMAIL,
        }
        
        html_content = render_to_string('accounts/emails/approval_confirmation.html', context)
        text_content = render_to_string('accounts/emails/approval_confirmation.txt', context)
        
        # Create email
        subject = 'Your Account Has Been Approved - Crown Data Portal'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return f"Approval confirmation sent to {user.email}"
        
    except User.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_rejection_notification_email(self, user_id, reason=''):
    """
    Send email to user notifying them their registration was rejected.
    
    Args:
        user_id: User's primary key
        reason: Optional reason for rejection
    """
    try:
        user = User.objects.get(pk=user_id)
        
        # Render email templates
        context = {
            'user': user,
            'reason': reason,
            'site_name': 'Crown Data Portal',
            'support_email': settings.SUPPORT_EMAIL,
        }
        
        html_content = render_to_string('accounts/emails/rejection_notification.html', context)
        text_content = render_to_string('accounts/emails/rejection_notification.txt', context)
        
        # Create email
        subject = 'Registration Update - Crown Data Portal'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return f"Rejection notification sent to {user.email}"
        
    except User.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
