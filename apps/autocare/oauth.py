import time
import requests
from django.conf import settings


class AutocareOAuthClient:
    _access_token = None
    _expires_at = 0

    @classmethod
    def get_access_token(cls):
        """
        Return a valid access token.
        Automatically refreshes if expired.
        """
        now = time.time()

        if cls._access_token and now < cls._expires_at:
            return cls._access_token

        cls._fetch_token()
        return cls._access_token

    @classmethod
    def _fetch_token(cls):
        response = requests.post(
            settings.AUTOCARE_OAUTH_TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": settings.AUTOCARE_CLIENT_ID,
                "client_secret": settings.AUTOCARE_CLIENT_SECRET,
                "username": settings.AUTOCARE_USERNAME,
                "password": settings.AUTOCARE_PASSWORD,
                "scope": settings.AUTOCARE_SCOPE,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=(5, 30),
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"OAuth token request failed\n"
                f"Status: {response.status_code}\n"
                f"Body: {response.text}"
            )

        payload = response.json()

        cls._access_token = payload["access_token"]
        cls._expires_at = time.time() + payload.get("expires_in", 3600) - 30

