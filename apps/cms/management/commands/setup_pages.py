from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Page, Site

from apps.cms.models import (
    HomePage,
    ProductIndexPage,
    CustomerDashboardPage,
    EmployeeDashboardPage,
    NewsletterIndexPage,
    ContentPage,
)

class Command(BaseCommand):
    help = "Initializes Wagtail pages safely and idempotently."

    def handle(self, *args, **options):
        self.stdout.write("=== Setting up Crown Nexus pages ===")

        # Repair treebeard before manipulating pages (dev only)
        if settings.DEBUG:
            call_command("fixtree", interactive=False)

        # 1) Root page
        root_page = Page.get_first_root_node()
        if not root_page:
            raise RuntimeError("Wagtail root page does not exist. Run migrations first.")
        self.stdout.write("  ✓ Wagtail root page found")

        # 2) Default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write("  → Creating default Site...")
            site = Site.objects.create(
                hostname="localhost",
                port=8000,
                site_name="Crown Nexus",
                root_page=root_page,
                is_default_site=True,
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Default Site created"))
        else:
            self.stdout.write("  ✓ Default Site exists")

        # 3) HomePage under root (delete wrong one first)
        homepage_ct = ContentType.objects.get_for_model(HomePage)

        wrong_home = (
            root_page.get_children()
            .filter(slug="home")
            .exclude(content_type=homepage_ct)
            .first()
        )
        if wrong_home:
            self.stdout.write("  → Removing invalid home page...")
            wrong_home.delete()
            root_page = Page.objects.get(pk=root_page.pk)  # reload parent

        home_page = root_page.get_children().type(HomePage).first()

        if not home_page:
            self.stdout.write("  → Creating HomePage...")
            home_page = HomePage(
                title="Home",
                slug="home",
                hero_title="Welcome to Crown Nexus",
                hero_subtitle="Your trusted source for quality automotive parts",
                intro="<p>Browse our extensive catalog of automotive parts.</p>",
                featured_section_title="Featured Products",
            )
            root_page.refresh_from_db()
            root_page.add_child(instance=home_page)
            home_page.save_revision().publish()
            home_page = HomePage.objects.get(pk=home_page.pk)  # reload after publish
            self.stdout.write(self.style.SUCCESS("    ✓ HomePage created"))
        else:
            self.stdout.write("  ✓ HomePage already exists")

        # 4) Force site root to HomePage
        if site.root_page_id != home_page.id:
            site.root_page = home_page
            site.save()
            self.stdout.write(self.style.SUCCESS("  ✓ HomePage set as Site root"))
        else:
            self.stdout.write("  ✓ HomePage already Site root")

        # Child helper
        def ensure_child(page_cls, slug, **fields):
            existing = home_page.get_children().type(page_cls).filter(slug=slug).first()
            if existing:
                self.stdout.write(f"  ✓ {page_cls.__name__} already exists")
                return existing

            self.stdout.write(f"  → Creating {page_cls.__name__}...")
            title = fields.pop("title", slug.replace("-", " ").title())
            p = page_cls(title=title, slug=slug, **fields)

            home_page.refresh_from_db()
            home_page.add_child(instance=p)
            p.save_revision().publish()

            self.stdout.write(self.style.SUCCESS(f"    ✓ {page_cls.__name__} created"))
            return p

        ensure_child(ProductIndexPage, "products", title="Products",
                     intro="<p>Browse our complete catalog of automotive parts.</p>")
        ensure_child(CustomerDashboardPage, "customer-dashboard", title="Customer Dashboard",
                     intro="<p>Manage your exports, validations, and account settings.</p>")
        ensure_child(EmployeeDashboardPage, "employee-dashboard", title="Employee Dashboard",
                     intro="<p>Access administrative tools and system monitoring.</p>")
        ensure_child(NewsletterIndexPage, "newsletters", title="Newsletters",
                     intro="<p>Latest product announcements and industry news.</p>")
        ensure_child(ContentPage, "about", title="About Us", body="[]")

        self.stdout.write(self.style.SUCCESS("\n✓ Crown Nexus pages fully initialized"))
