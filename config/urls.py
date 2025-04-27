# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from supervisor_dashboard.admin import supervisor_admin_site

urlpatterns = [
    # Custom Supervisor AdminSite
    path('admin/', supervisor_admin_site.urls),

    # API endpoints
    path('api/', include('announcements.urls')),
    path('api/', include('votes.urls')),
    path('api/requests/', include('user_requests.urls')),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/tenants/', include('tenants.urls')),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Django’s built-in auth URLs (for /accounts/... )
    path('accounts/', include('django.contrib.auth.urls')),
]
