"""
Template tags for CMS navigation and utilities.
"""

from django import template
from wagtail.models import Page

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_nav(context):
    """
    Get navigation menu based on user authentication and role.
    """
    request = context["request"]
    user = request.user

    # Start with main navigation
    nav_items = []

    # Home
    try:
        home = Page.objects.filter(depth=2).first()
        if home:
            nav_items.append(
                {"url": home.url, "title": "Home", "active": request.path == home.url}
            )
    except:
        pass

    # Products - always visible
    try:
        from apps.cms.models import ProductIndexPage

        product_page = ProductIndexPage.objects.live().first()
        if product_page:
            nav_items.append(
                {
                    "url": product_page.url,
                    "title": "Products",
                    "active": request.path.startswith(product_page.url),
                }
            )
    except:
        pass

    # Authenticated user items
    if user.is_authenticated:
        # Customer-specific
        if user.is_customer:
            try:
                from apps.cms.models import CustomerDashboardPage

                dashboard = CustomerDashboardPage.objects.live().first()
                if dashboard:
                    nav_items.append(
                        {
                            "url": dashboard.url,
                            "title": "My Dashboard",
                            "active": request.path == dashboard.url,
                        }
                    )
            except:
                pass

            # Exports
            nav_items.append(
                {
                    "url": "/exports/",
                    "title": "Exports",
                    "active": request.path.startswith("/exports/"),
                }
            )

            # Validator
            nav_items.append(
                {
                    "url": "/validator/",
                    "title": "Validator",
                    "active": request.path.startswith("/validator/"),
                }
            )

        # Employee-specific
        if user.is_employee:
            try:
                from apps.cms.models import EmployeeDashboardPage

                dashboard = EmployeeDashboardPage.objects.live().first()
                if dashboard:
                    nav_items.append(
                        {
                            "url": dashboard.url,
                            "title": "Employee Dashboard",
                            "active": request.path == dashboard.url,
                        }
                    )
            except:
                pass

            # Admin
            nav_items.append(
                {
                    "url": "/admin/",
                    "title": "Admin",
                    "active": request.path.startswith("/admin/"),
                }
            )

            # CMS
            nav_items.append(
                {
                    "url": "/cms/",
                    "title": "CMS",
                    "active": request.path.startswith("/cms/"),
                }
            )

    # Newsletter (always visible)
    try:
        from apps.cms.models import NewsletterIndexPage

        newsletter_page = NewsletterIndexPage.objects.live().first()
        if newsletter_page:
            nav_items.append(
                {
                    "url": newsletter_page.url,
                    "title": "Newsletters",
                    "active": request.path.startswith(newsletter_page.url),
                }
            )
    except:
        pass

    return nav_items


@register.simple_tag(takes_context=True)
def get_user_menu(context):
    """
    Get user-specific menu items.
    """
    request = context["request"]
    user = request.user

    if not user.is_authenticated:
        return [
            {"url": "/accounts/login/", "title": "Login", "icon": "sign-in-alt"},
            {"url": "/accounts/register/", "title": "Register", "icon": "user-plus"},
        ]

    menu_items = [
        {"url": "/accounts/profile/", "title": "Profile", "icon": "user"},
        {"url": "/accounts/logout/", "title": "Logout", "icon": "sign-out-alt"},
    ]

    return menu_items


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary."""
    return dictionary.get(key)
