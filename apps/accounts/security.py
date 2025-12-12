from django.shortcuts import redirect
from django.urls import reverse
from django_otp import user_has_device


def user_requires_2fa(user):
    """
    Define which users MUST have 2FA.
    """
    if not user.is_authenticated:
        return False

    # Staff must always have 2FA
    if user.is_staff:
        return True

    # Employees must always have 2FA
    if getattr(user, "is_employee", False):
        return True

    return False


def enforce_2fa(view_func):
    """
    Decorator that forces 2FA enrollment if required.
    """
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if user_requires_2fa(user) and not user_has_device(user):
            return redirect(
                reverse("two_factor:setup")
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view
