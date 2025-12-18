import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from django.conf import settings
from apps.autocare.oauth import AutocareOAuthClient


class AutocareAPIError(Exception):
    """Base Autocare API error."""


class AutocareAPIRetryableError(AutocareAPIError):
    """Transient error (safe to retry)."""


class AutocareAPIFatalError(AutocareAPIError):
    """Permanent error (do not retry)."""


class AutocareAPIClient:
    """
    Resilient Autocare API client.

    - Automatic retries with backoff
    - Supports absolute pagination URLs
    - Safe for Celery + long-running ingestion
    """

    def __init__(self):
        self.base_url = settings.VCDB_API_BASE.rstrip("/")
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()

        retry = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=1.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retry,
            pool_connections=20,
            pool_maxsize=20,
        )

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        token = AutocareOAuthClient.get_access_token()

        # Handle absolute pagination URLs
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{self.base_url}{path}"

        try:
            response = self.session.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=(5, 180),  # (connect, read)
            )
        except requests.exceptions.Timeout as exc:
            raise AutocareAPIRetryableError(f"Timeout fetching {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AutocareAPIRetryableError(f"Connection error fetching {url}") from exc

        # Explicit status handling
        if response.status_code == 401:
            raise AutocareAPIFatalError("Unauthorized (invalid OAuth token)")
        if response.status_code == 403:
            raise AutocareAPIFatalError("Forbidden (permission issue)")
        if response.status_code == 404:
            raise AutocareAPIFatalError(f"Endpoint not found: {url}")
        if response.status_code >= 500:
            raise AutocareAPIRetryableError(
                f"Server error {response.status_code} from {url}"
            )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise AutocareAPIError(
                f"HTTP error {response.status_code} from {url}"
            ) from exc

        return response
