from wagtail import hooks
from django.urls import path
from django.core.exceptions import PermissionDenied
from apps.cms.models import ArchivedNewsletterPage

from apps.cms.admin.mailchimp_import import MailchimpImportView
from apps.cms.admin.menu import MailchimpImportMenuItem

@hooks.register("before_edit_page")
def prevent_editing_archived_newsletters(request, page):
    if isinstance(page.specific, ArchivedNewsletterPage):
        raise PermissionDenied(
            "Archived newsletters are immutable and cannot be edited."
        )

@hooks.register("construct_page_action_menu")
def hide_edit_actions_for_archived(menu_items, request, context):
    page = context.get("page")
    if isinstance(page.specific, ArchivedNewsletterPage):
        menu_items[:] = [
            item for item in menu_items
            if item.name not in {"save", "publish"}
        ]

@hooks.register("register_page_action_menu_item")
def register_mailchimp_import_menu_item():
    return MailchimpImportMenuItem()

@hooks.register("register_admin_urls")
def register_mailchimp_admin_urls():
    return [
        path(
            "mailchimp/import/<int:parent_id>/",
            MailchimpImportView.as_view(),
            name="mailchimp_import",
        )
    ]
