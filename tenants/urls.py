# tenants/urls.py ✅

from django.urls import path
from tenants.views import TenantListView, TenantDetailView, TenantCreateView

urlpatterns = [
    path("", TenantListView.as_view(), name="tenant-list"),
    path("<int:pk>/", TenantDetailView.as_view(), name="tenant-detail"),
    path("create/", TenantCreateView.as_view(), name="tenant-create"),
]
