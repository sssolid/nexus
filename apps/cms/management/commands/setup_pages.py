"""
Management command to set up initial Wagtail pages for Crown Nexus.
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from apps.cms.models import (
    ContentPage,
    CustomerDashboardPage,
    EmployeeDashboardPage,
    HomePage,
    NewsletterIndexPage,
    ProductIndexPage,
)


class Command(BaseCommand):
    help = "Set up initial Wagtail pages for Crown Nexus"

    def handle(self, *args, **options):
        self.stdout.write("Setting up Crown Nexus pages...")

        # Get the root page
        root_page = Page.get_first_root_node()

        ######################################################################
        # HOME PAGE
        ######################################################################
        # Find existing "home" under the root
        existing_home = root_page.get_children().filter(slug="home").first()

        if existing_home:
            if isinstance(existing_home.specific, HomePage):
                home_page = existing_home.specific
                self.stdout.write("  → Home page already exists")
            else:
                self.stdout.write("  → Existing 'home' page is not HomePage; deleting it...")
                existing_home.delete()
                existing_home = None

        # Create if missing
        if not existing_home:
            self.stdout.write("Creating Home Page...")
            home_page = HomePage(
                title="Home",
                slug="home",
                hero_title="Welcome to Crown Nexus",
                hero_subtitle="Your trusted source for quality automotive parts",
                intro="<p>Browse our extensive catalog of automotive parts and accessories.</p>",
                featured_section_title="Featured Products",
            )
            root_page.add_child(instance=home_page)
            home_page.save_revision().publish()

            # Always enforce site root, even if the page already existed
            site = Site.objects.filter(is_default_site=True).first()
            if site.root_page_id != home_page.id:
                site.root_page = home_page
                site.save()
                self.stdout.write(self.style.SUCCESS("  ✓ Home page set as site root"))
            else:
                self.stdout.write("  → Home page already set as site root")

        ######################################################################
        # PRODUCT INDEX
        ######################################################################
        if not home_page.get_children().filter(slug="products").exists():
            self.stdout.write("Creating Product Index Page...")
            product_page = ProductIndexPage(
                title="Products",
                slug="products",
                intro="<p>Browse our complete catalog of automotive parts.</p>",
            )
            home_page.add_child(instance=product_page)
            product_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("  ✓ Product index page created"))
        else:
            self.stdout.write("  → Product index page already exists")

        ######################################################################
        # CUSTOMER DASHBOARD
        ######################################################################
        if not home_page.get_children().filter(slug="customer-dashboard").exists():
            self.stdout.write("Creating Customer Dashboard Page...")
            customer_dashboard = CustomerDashboardPage(
                title="Customer Dashboard",
                slug="customer-dashboard",
                intro="<p>Welcome to your dashboard. Manage your exports, validations, and account settings.</p>",
            )
            home_page.add_child(instance=customer_dashboard)
            customer_dashboard.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("  ✓ Customer dashboard created"))
        else:
            self.stdout.write("  → Customer dashboard already exists")

        ######################################################################
        # EMPLOYEE DASHBOARD
        ######################################################################
        if not home_page.get_children().filter(slug="employee-dashboard").exists():
            self.stdout.write("Creating Employee Dashboard Page...")
            employee_dashboard = EmployeeDashboardPage(
                title="Employee Dashboard",
                slug="employee-dashboard",
                intro="<p>Access administrative tools and system monitoring.</p>",
            )
            home_page.add_child(instance=employee_dashboard)
            employee_dashboard.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("  ✓ Employee dashboard created"))
        else:
            self.stdout.write("  → Employee dashboard already exists")

        ######################################################################
        # NEWSLETTER INDEX
        ######################################################################
        if not home_page.get_children().filter(slug="newsletters").exists():
            self.stdout.write("Creating Newsletter Index Page...")
            newsletter_index = NewsletterIndexPage(
                title="Newsletters",
                slug="newsletters",
                intro="<p>Stay updated with our latest product announcements and industry news.</p>",
            )
            home_page.add_child(instance=newsletter_index)
            newsletter_index.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("  ✓ Newsletter index created"))
        else:
            self.stdout.write("  → Newsletter index already exists")

        ######################################################################
        # ABOUT PAGE
        ######################################################################
        if not home_page.get_children().filter(slug="about").exists():
            self.stdout.write("Creating About Page...")
            about_page = ContentPage(
                title="About Us",
                slug="about",
                body="[]",
            )
            home_page.add_child(instance=about_page)
            about_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("  ✓ About page created"))
        else:
            self.stdout.write("  → About page already exists")

        ######################################################################
        # DONE
        ######################################################################
        self.stdout.write(self.style.SUCCESS("\n✓ Page setup complete!"))
        self.stdout.write("\nNext steps:")
        self.stdout.write("1. Visit /cms/ to edit content")
        self.stdout.write("2. Add featured products in Django admin")
        self.stdout.write("3. Configure navigation and branding")
