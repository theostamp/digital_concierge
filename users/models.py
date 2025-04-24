# users/models.py
from django.conf import settings
from django.db import models
from buildings.models import Building
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({'Supervisor' if self.is_supervisor else 'Tenant User'})"


class UserProfile(models.Model):
    USER_ROLES = (
        ('resident', 'Resident'),
        ('manager', 'Building Manager'),
        ('tech', 'Technician'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='resident')
    phone = models.CharField(max_length=20, blank=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
