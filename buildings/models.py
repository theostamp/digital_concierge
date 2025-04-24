from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    label = models.CharField(max_length=100, help_text="e.g., Main Entrance Tablet")
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    unique_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.label} in {self.building.name}"
