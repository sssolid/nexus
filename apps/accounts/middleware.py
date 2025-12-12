from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django_otp import user_has_device


class Enforce2FAMiddleware(MiddlewareMixin):
    """
    Enforce 2FA for staff and employees on protected routes.
    Customers are blocked entirely from admin/CMS.
    """

    PROTECTED_PREFIXES = (
        "/admin/",
        "/cms/",
        "/documents/",
    )

    ALLOW_PREFIXES = (
        "/auth/",                # two_factor URLs
        "/accounts/logout/",
        "/static/",
        "/media/",
        "/health/",
        "/__debug__/",
    )

    def is_protected_path(self, path: str) -> bool:
        return path.startswith(self.PROTECTED_PREFIXES)

    def is_allowed_path(self, path: str) -> bool:
        return path.startswith(self.ALLOW_PREFIXES)

    def user_requires_2fa(self, user) -> bool:
        """
        Only staff and employees are required to use 2FA.
        """
        return (
            user.is_authenticated
            and (user.is_staff or getattr(user, "is_employee", False))
        )

    def process_request(self, request):
        path = request.path
        user = request.user

        # Always allow explicitly allowed paths
        if self.is_allowed_path(path):
            return None

        # Protect admin / CMS routes
        if self.is_protected_path(path):

            # Not logged in → login
            if not user.is_authenticated:
                return redirect(reverse("two_factor:login"))

            # Logged in but NOT employee/staff → hard block
            if not getattr(user, "is_employee", False) and not user.is_staff:
                return redirect(reverse("accounts:profile"))

            # Employee/staff → must have 2FA
            if self.user_requires_2fa(user):

                # No device enrolled
                if not user_has_device(user):
                    return redirect(reverse("two_factor:setup"))

                # Device exists but session NOT OTP verified
                if not getattr(user, "is_verified", lambda: False)():
                    return redirect(reverse("two_factor:login"))

        return None
