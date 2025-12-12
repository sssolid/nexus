from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django_otp import user_has_device


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mint_token(request):
    user = request.user

    # Safety: must have OTP device
    if not user_has_device(user):
        return Response(
            {"detail": "2FA enrollment required."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Safety: must have verified OTP this session
    try:
        if not user.email_verified():
            return Response(
                {"detail": "2FA verification required."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except Exception:
        return Response(
            {"detail": "2FA verification required."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Safety: must be approved
    if not getattr(user, "is_approved", False):
        return Response(
            {"detail": "Account not approved."},
            status=status.HTTP_403_FORBIDDEN,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "user": user.email,
        },
        status=status.HTTP_200_OK,
    )
