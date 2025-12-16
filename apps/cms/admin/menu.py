from django.urls import reverse
from wagtail.admin.action_menu import ActionMenuItem
from apps.cms.models import NewsletterIndexPage


class MailchimpImportMenuItem(ActionMenuItem):
    name = "mailchimp_import"   # ← THIS IS REQUIRED
    label = "Import from Mailchimp"
    classname = "button-secondary"
    order = 50
    permissions = ["wagtailadmin.access_admin"]

    def is_shown(self, context):
        page = context.get("page")
        return isinstance(page, NewsletterIndexPage)

    def get_url(self, context):
        return reverse("mailchimp_import", args=[context["page"].id])
