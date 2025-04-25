# tenants/urls.py
from django.urls import path
from .views import TenantListView

urlpatterns = [
    path("", TenantListView.as_view(), name="tenant-list"),
]
