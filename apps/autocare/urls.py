from django.urls import include, path

urlpatterns = [
    path("vcdb/", include("apps.autocare.urls.vcdb")),
]
