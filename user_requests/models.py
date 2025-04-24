from django.db import models
from django.contrib.auth import get_user_model

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Εκκρεμεί'),
        ('completed', 'Ολοκληρώθηκε'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_requests')

    def __str__(self):
        return self.title
