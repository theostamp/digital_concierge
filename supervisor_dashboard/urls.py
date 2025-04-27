from django.urls import path, include
from supervisor_dashboard.admin import supervisor_admin_site

urlpatterns = [
    path('admin/dashboard/', supervisor_admin_site.urls),
    path('', supervisor_admin_site.urls),
]