import requests
from django.conf import settings

class MailchimpClient:
    def __init__(self):
        self.base_url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0"
        self.auth = ("anystring", settings.MAILCHIMP_API_KEY)

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()