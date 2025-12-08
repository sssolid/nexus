"""
Wagtail CMS page models for Crown Nexus.

Provides unified content management for marketing pages,
product catalog integration, and role-based dashboards.
"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

from apps.products.models import Product, ProductCategory


class HomePage(Page):
    """
    Home page with featured products and hero content.
    """

    hero_title = models.CharField(max_length=255, default="Welcome to Crown Nexus")
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    intro = RichTextField(blank=True)

    # Featured content
    featured_section_title = models.CharField(
        max_length=255, default="Featured Products"
    )

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("html", blocks.RawHTMLBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_image"),
            ],
            heading="Hero Section",
        ),
        FieldPanel("intro"),
        FieldPanel("featured_section_title"),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        """Add featured products to context."""
        context = super().get_context(request)

        # Get featured products
        context["featured_products"] = (
            Product.objects.filter(is_featured=True, is_active=True)
            .select_related("category", "manufacturer")
            .prefetch_related("images")[:6]
        )

        # Get categories
        context["categories"] = ProductCategory.objects.filter(
            is_active=True, parent=None
        )[:6]

        return context

    class Meta:
        verbose_name = "Home Page"


class ProductIndexPage(Page):
    """
    Product catalog index page integrated with Wagtail.
    """

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = []  # No child pages

    def get_context(self, request):
        """Get product listings with filtering."""
        context = super().get_context(request)

        # Get products with filters
        products = (
            Product.objects.filter(is_active=True)
            .select_related("category", "manufacturer")
            .prefetch_related("images")
        )

        # Search
        search = request.GET.get("search")
        if search:
            products = products.filter(
                models.Q(part_number__icontains=search)
                | models.Q(manufacturer_part_number__icontains=search)
                | models.Q(name__icontains=search)
                | models.Q(description__icontains=search)
            )

        # Filter by category
        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        # Filter by manufacturer
        manufacturer_id = request.GET.get("manufacturer")
        if manufacturer_id:
            products = products.filter(manufacturer_id=manufacturer_id)

        # Filter by status
        status = request.GET.get("status")
        if status:
            products = products.filter(status=status)

        # Pagination
        paginator = Paginator(products, 50)
        page = request.GET.get("page")

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context["products"] = products
        context["categories"] = ProductCategory.objects.filter(is_active=True)
        context["manufacturers"] = products.model.objects.values_list(
            "manufacturer", flat=True
        ).distinct()

        return context

    class Meta:
        verbose_name = "Product Index Page"


class CustomerDashboardPage(Page):
    """
    Customer-specific dashboard page.
    """

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = []

    def serve(self, request):
        """Require customer authentication."""
        if not request.user.is_authenticated or not request.user.is_customer:
            from django.shortcuts import redirect

            return redirect("accounts:login")
        return super().serve(request)

    def get_context(self, request):
        """Add customer-specific context."""
        context = super().get_context(request)

        if request.user.is_authenticated:
            # Recent export jobs
            context["recent_exports"] = request.user.export_jobs.all()[:5]

            # Recent validation jobs
            context["recent_validations"] = request.user.validation_jobs.all()[:5]

        return context

    class Meta:
        verbose_name = "Customer Dashboard"


class EmployeeDashboardPage(Page):
    """
    Employee-specific dashboard page.
    """

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = []

    def serve(self, request):
        """Require employee authentication."""
        if not request.user.is_authenticated or not request.user.is_employee:
            from django.shortcuts import redirect

            return redirect("accounts:login")
        return super().serve(request)

    def get_context(self, request):
        """Add employee-specific context."""
        context = super().get_context(request)

        if request.user.is_authenticated:
            from apps.data_sync.models import SyncJob
            from apps.exports.models import ExportJob

            # Recent sync jobs
            context["recent_syncs"] = SyncJob.objects.all()[:5]

            # Export statistics
            context["total_exports"] = ExportJob.objects.filter(
                status="COMPLETED"
            ).count()

        return context

    class Meta:
        verbose_name = "Employee Dashboard"


class ContentPage(Page):
    """
    Generic content page for about, contact, etc.
    """

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("html", blocks.RawHTMLBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    class Meta:
        verbose_name = "Content Page"


class NewsletterIndexPage(Page):
    """
    Newsletter archive index page.
    """

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["cms.NewsletterPage"]

    def get_context(self, request):
        """Get newsletter listings."""
        context = super().get_context(request)

        # Get published newsletters
        newsletters = (
            NewsletterPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )

        # Pagination
        paginator = Paginator(newsletters, 10)
        page = request.GET.get("page")

        try:
            newsletters = paginator.page(page)
        except PageNotAnInteger:
            newsletters = paginator.page(1)
        except EmptyPage:
            newsletters = paginator.page(paginator.num_pages)

        context["newsletters"] = newsletters
        return context

    class Meta:
        verbose_name = "Newsletter Index"


class NewsletterPage(Page):
    """
    Individual newsletter page.
    """

    date = models.DateField("Newsletter date")
    intro = models.CharField(max_length=500)

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    parent_page_types = ["cms.NewsletterIndexPage"]

    class Meta:
        verbose_name = "Newsletter"
        ordering = ["-date"]
