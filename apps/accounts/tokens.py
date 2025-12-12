"""
Token generation and verification for email validation.
"""
import secrets


def generate_verification_token():
    """
    Generate a secure random token for email verification.
    
    Returns:
        str: A URL-safe token string
    """
    return secrets.token_urlsafe(32)
