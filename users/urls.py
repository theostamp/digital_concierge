# users\urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import current_user, CustomPasswordChangeView

urlpatterns = [
    path('me/', current_user),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
