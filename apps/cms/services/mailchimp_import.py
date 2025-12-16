from django.utils.dateparse import parse_datetime
from wagtail.models import Page
from apps.cms.models import ArchivedNewsletterPage
from services.mailchimp import MailchimpClient

class MailchimpImporter:
    def __init__(self, parent_page):
        self.client = MailchimpClient()
        self.parent_page = parent_page

    def list_sent_campaigns(self, limit=50):
        data = self.client.get(
            "/campaigns",
            params={
                "status": "sent",
                "count": limit,
                "sort_field": "send_time",
                "sort_dir": "DESC",
            },
        )
        return data["campaigns"]

    def import_campaign(self, campaign):
        campaign_id = campaign["id"]

        if ArchivedNewsletterPage.objects.filter(
            mailchimp_campaign_id=campaign_id
        ).exists():
            raise ValueError("Campaign already imported")

        content = self.client.get(f"/campaigns/{campaign_id}/content")

        page = ArchivedNewsletterPage(
            title=campaign["settings"]["subject_line"],
            subject=campaign["settings"]["subject_line"],
            send_date=parse_datetime(campaign["send_time"]),
            mailchimp_campaign_id=campaign_id,
            archive_url=campaign.get("archive_url", ""),
            html_content=content["html"],
        )

        page._importing = True

        self.parent_page.add_child(instance=page)
        page.save_revision()

        return page
