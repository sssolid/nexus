"""
URL configuration for the accounts application.
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views, views_verification

app_name = "accounts"

urlpatterns = [
    # --------------------------------------------------------
    # Logout (safe to keep)
    # --------------------------------------------------------
    path(
        "logout/",
        LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),

    # --------------------------------------------------------
    # Registration and verification
    # --------------------------------------------------------
    path("register/", views_verification.UserRegistrationView.as_view(), name="register"),
    path("verify-email/<str:token>/", views_verification.verify_email_view, name="verify_email"),
    path("verification-sent/", views_verification.verification_sent_view, name="verification_sent"),
    path(
        "verification-success/",
        views_verification.verification_success_view,
        name="verification_success",
    ),
    path(
        "resend-verification/",
        views_verification.resend_verification_view,
        name="resend_verification",
    ),

    # --------------------------------------------------------
    # Legacy / informational
    # --------------------------------------------------------
    path(
        "registration-pending/",
        views.registration_pending_view,
        name="registration_pending",
    ),

    # --------------------------------------------------------
    # Profile
    # --------------------------------------------------------
    path("profile/", views.profile_view, name="profile"),

    # --------------------------------------------------------
    # Approval management
    # --------------------------------------------------------
    path(
        "approvals/",
        views_verification.pending_approvals_list_view,
        name="pending_approvals_list",
    ),
    path(
        "approvals/<int:user_id>/approve/",
        views_verification.approve_registration_view,
        name="approve_user",
    ),
    path(
        "approvals/<int:user_id>/reject/",
        views_verification.reject_registration_view,
        name="reject_user",
    ),
]
