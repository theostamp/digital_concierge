# 📄 config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('announcements.urls')),
    path('api/', include('votes.urls')),
    path('api/requests/', include('user_requests.urls')),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # ✅ Προσθήκη auth routes (login, logout, password change/reset)
    path('accounts/', include('django.contrib.auth.urls')),
]
