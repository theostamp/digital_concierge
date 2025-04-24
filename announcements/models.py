# 📄 announcements/models.py

from django.db import models

class Announcement(models.Model):
    TYPE_CHOICES = [
        ('manager', 'Γραφείο Διαχείρισης'),
        ('internal', 'Εσωτερικός Διαχειριστής'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='manager')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
