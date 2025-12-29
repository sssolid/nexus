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

    def __init__(self, dataset: str):
        self.api_host = settings.VCDB_API_HOST.rstrip("/")
        self.api_host = settings.AUTOCARE_API_HOSTS[dataset].rstrip("/")
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

        # Absolute pagination URL
        if path.startswith("http"):
            url = path
        elif path.startswith("/api/"):
            url = f"{self.api_host}{path}"
        else:
            raise ValueError(f"Path must start with /api/. Got: {path}")

        try:
            response = self.session.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=(5, 180),
            )
        except requests.exceptions.Timeout as exc:
            raise AutocareAPIRetryableError(f"Timeout fetching {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AutocareAPIRetryableError(f"Connection error fetching {url}") from exc

        if response.status_code == 401:
            raise AutocareAPIFatalError("Unauthorized (invalid OAuth token)")
        if response.status_code == 403:
            raise AutocareAPIFatalError("Forbidden (permission issue)")
        if response.status_code == 404:
            raise AutocareAPIFatalError(f"Endpoint not found: {url}")
        if response.status_code >= 500:
            raise AutocareAPIRetryableError(f"Server error {response.status_code} from {url}")

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise AutocareAPIError(f"HTTP error {response.status_code} from {url}") from exc

        return response

    def get_raw(self, raw_path: str, params: dict | None = None) -> requests.Response:
        """
        GET a raw API path under the host WITHOUT forcing /api/v1.0.
        Used for UI-style endpoints like /api/vcdb/vehicles/{id}.

        Must reuse:
          - OAuth token
          - headers
          - retry session
          - timeout semantics
        """
        if not raw_path.startswith("/api/"):
            raise ValueError(f"raw_path must start with /api/. Got: {raw_path}")

        token = AutocareOAuthClient.get_access_token()
        url = f"{self.api_host}{raw_path}"

        try:
            response = self.session.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=(5, 180),  # SAME AS get()
            )
        except requests.exceptions.Timeout as exc:
            raise AutocareAPIRetryableError(f"Timeout fetching {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AutocareAPIRetryableError(f"Connection error fetching {url}") from exc

        # Match get() semantics exactly
        if response.status_code == 401:
            raise AutocareAPIFatalError("Unauthorized (invalid OAuth token)")
        if response.status_code == 403:
            raise AutocareAPIFatalError("Forbidden (permission issue)")
        if response.status_code == 404:
            return response  # caller handles missing
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

