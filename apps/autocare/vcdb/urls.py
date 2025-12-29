from django.urls import path
from apps.autocare.vcdb.views import VCdbListView, VCdbDetailView


app_name = "autocare_vcdb"

urlpatterns = [
    path("<str:model>/", VCdbListView.as_view(), name="vcdb-list"),
    path("<str:model>/<int:pk>/", VCdbDetailView.as_view(), name="vcdb-detail"),
]
