"""
URL Configuration for Crown Nexus System.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Wagtail CMS
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # App URLs
    path('accounts/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('aces-pies/', include('apps.aces_pies.urls')),
    path('exports/', include('apps.exports.urls')),
    path('validator/', include('apps.validator.urls')),
    path('media-library/', include('apps.media_library.urls')),
    
    # API URLs
    path('api/v1/', include('apps.api.urls')),
    
    # Health check
    path('health/', include('health_check.urls')),
    
    # Wagtail pages (should be last to catch all remaining URLs)
    path('', include(wagtail_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Django Debug Toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Custom error handlers
handler400 = 'apps.accounts.views.error_400'
handler403 = 'apps.accounts.views.error_403'
handler404 = 'apps.accounts.views.error_404'
handler500 = 'apps.accounts.views.error_500'
