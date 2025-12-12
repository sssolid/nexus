"""URL configuration for the API application."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_token import mint_token

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path("auth/token/", mint_token, name="mint_token"),
    path('', include(router.urls)),
]
