from django.db import models
from django.contrib.auth.models import User

class ListeningSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top_tracks = models.JSONField()
    top_artists = models.JSONField()
    top_genres = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Listening Summary"