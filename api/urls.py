# api/urls.py ✅

from django.urls import path, include

urlpatterns = [
    path("tenants/", include("tenants.urls")),
]
