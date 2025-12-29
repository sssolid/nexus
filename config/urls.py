"""
URL Configuration for Crown Nexus System.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from two_factor import urls as two_factor_urls

from django.contrib import admin
from django_otp.admin import OTPAdminSite

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.cms import views as static_views

# ------------------------------------------------------------
# OTP-protected Django admin
# ------------------------------------------------------------


admin.autodiscover()  # make sure admin modules are loaded

otp_admin_site = OTPAdminSite(name="otp_admin")

# Copy everything registered on the default admin into the OTP admin
otp_admin_site._registry.update(admin.site._registry)

urlpatterns = [
    # --------------------------------------------------------
    # Django Admin (OTP protected)
    # --------------------------------------------------------
    path("admin/", otp_admin_site.urls),

    # --------------------------------------------------------
    # Two-Factor Authentication (LOGIN SOURCE OF TRUTH)
    # --------------------------------------------------------
    path("auth/", include(two_factor_urls.urlpatterns)),

    # --------------------------------------------------------
    # Wagtail Admin
    # (Relies on Django auth + OTP middleware)
    # --------------------------------------------------------
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    # --------------------------------------------------------
    # API Documentation
    # --------------------------------------------------------
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # --------------------------------------------------------
    # Application URLs
    # --------------------------------------------------------
    path("accounts/", include("apps.accounts.urls")),
    path("products/search/", include("apps.products.urls")),
    path("aces-pies/", include("apps.aces_pies.urls")),
    path("exports/", include("apps.exports.urls")),
    path("validator/", include("apps.validator.urls")),
    path("media-library/", include("apps.media_library.urls")),

    # --------------------------------------------------------
    # API
    # --------------------------------------------------------
    path("api/v1/", include("apps.api.urls")),

    # --------------------------------------------------------
    # Health check
    # --------------------------------------------------------
    path("health/", include("health_check.urls")),

    # --------------------------------------------------------
    # Static informational pages
    # --------------------------------------------------------
    path("terms/", static_views.terms_of_service, name="terms"),
    path("privacy/", static_views.privacy_policy, name="privacy"),
    path("contact/", static_views.contact_us, name="contact"),

    # --------------------------------------------------------
    # Autocare pages
    # --------------------------------------------------------
    path("vcdb/", include("apps.autocare.vcdb.urls", namespace="vcdb")),

    # --------------------------------------------------------
    # Wagtail pages (MUST BE LAST)
    # --------------------------------------------------------
    path("", include(wagtail_urls)),
]

# ------------------------------------------------------------
# Development-only static & debug
# ------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns.insert(
            0,
            path("__debug__/", include(debug_toolbar.urls)),
        )

# ------------------------------------------------------------
# Error handlers (moved out of accounts)
# ------------------------------------------------------------
handler400 = "config.views.error_400"
handler403 = "config.views.error_403"
handler404 = "config.views.error_404"
handler500 = "config.views.error_500"
