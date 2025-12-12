"""
Token generation and verification for email validation.
"""
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils import timezone


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for email verification.
    Uses Django's built-in token generation with custom key salt.
    """
    
    def _make_hash_value(self, user, timestamp):
        """
        Create hash value for token generation.
        Includes user's pk, email, and is_verified status.
        """
        return (
            str(user.pk) + 
            user.email + 
            str(user.is_verified) + 
            str(timestamp)
        )


email_verification_token = EmailVerificationTokenGenerator()


def generate_verification_token():
    """
    Generate a secure random token for email verification.
    
    Returns:
        str: A URL-safe token string
    """
    return secrets.token_urlsafe(32)


def create_signed_token(user_id, token):
    """
    Create a signed token that includes the user ID.
    
    Args:
        user_id: User's primary key
        token: Verification token
        
    Returns:
        str: Signed token string
    """
    signer = TimestampSigner()
    value = f"{user_id}:{token}"
    return signer.sign(value)


def verify_signed_token(signed_token, max_age=None):
    """
    Verify a signed token and extract user ID and token.
    
    Args:
        signed_token: The signed token to verify
        max_age: Maximum age in seconds (default: 24 hours)
        
    Returns:
        tuple: (user_id, token) if valid, (None, None) if invalid
        
    Raises:
        SignatureExpired: If token has expired
        BadSignature: If token is invalid
    """
    if max_age is None:
        max_age = getattr(settings, 'EMAIL_VERIFICATION_TIMEOUT', 86400)  # 24 hours
    
    signer = TimestampSigner()
    try:
        unsigned_value = signer.unsign(signed_token, max_age=max_age)
        user_id, token = unsigned_value.split(':', 1)
        return int(user_id), token
    except (BadSignature, SignatureExpired, ValueError):
        return None, None
