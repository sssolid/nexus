from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied


class VerifiedApprovedBackend(ModelBackend):
    """
    Authentication backend that blocks login unless the user
    is verified AND approved.
    """

    def user_can_authenticate(self, user):
        """
        Override Django's default check.
        """
        if not super().user_can_authenticate(user):
            return False

        # Block unverified users
        if not getattr(user, "email_verified", False):
            return False

        # Block unapproved users
        if not getattr(user, "is_approved", False):
            return False

        return True
