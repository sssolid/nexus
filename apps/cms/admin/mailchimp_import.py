# cms/admin/mailchimp_import.py

from django.views.generic import TemplateView
from wagtail.admin.views.generic import WagtailAdminTemplateMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from wagtail.models import Page

from apps.cms.services.mailchimp_import import MailchimpImporter


class MailchimpImportView(WagtailAdminTemplateMixin, TemplateView):
    template_name = "cms/admin/mailchimp_import.html"
    page_title = "Import Mailchimp Campaign"

    def dispatch(self, request, *args, **kwargs):
        self.parent_page = Page.objects.get(id=kwargs["parent_id"]).specific
        self.importer = MailchimpImporter(self.parent_page)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        campaigns = self.importer.list_sent_campaigns()
        return self.render_to_response({
            "campaigns": campaigns,
            "parent": self.parent_page,
        })

    def post(self, request, *args, **kwargs):
        campaign_ids = request.POST.getlist("campaign_ids")

        campaigns = self.importer.list_sent_campaigns()

        imported = 0
        skipped = 0

        for campaign in campaigns:
            if campaign["id"] not in campaign_ids:
                continue

            try:
                self.importer.import_campaign(campaign)
                imported += 1
            except ValueError:
                skipped += 1

        messages.success(
            request,
            f"Imported {imported} newsletter(s). Skipped {skipped} already imported."
        )

        return redirect("wagtailadmin_explore", self.parent_page.id)

