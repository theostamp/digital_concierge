# 📄 votes/models.py

from django.db import models
from django.contrib.auth import get_user_model
from buildings.models import Building

User = get_user_model()

class Vote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='votes')

    def __str__(self):
        return self.title

class VoteOption(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vote.title} - {self.text}"

class VoteAnswer(models.Model):
    option = models.ForeignKey(VoteOption, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('option', 'user')  # Ψήφος μία φορά ανά χρήστη ανά επιλογή

    def __str__(self):
        return f"{self.user.username} voted {self.option.text}"
