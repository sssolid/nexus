import requests
from django.conf import settings
from apps.autocare.oauth import AutocareOAuthClient


class AutocareAPIClient:
    def __init__(self):
        self.base_url = settings.VCDB_API_BASE.rstrip("/")
        self.session = requests.Session()

    def get(self, path, params=None):
        token = AutocareOAuthClient.get_access_token()

        # IMPORTANT: handle absolute pagination URLs
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{self.base_url}{path}"

        response = self.session.get(
            url,
            params=params,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=(5, 90),
        )
        response.raise_for_status()
        return response
