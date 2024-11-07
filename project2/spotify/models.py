from django.db import models
from django.contrib.auth.models import User

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.IntegerField(default=60)
    token_type = models.CharField(max_length=50)

class UserSpotifyLink(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_user_id = models.CharField(max_length=255, unique=True)  # Spotify user ID

    def __str__(self):
        return f"{self.user.username} - {self.spotify_user_id}"
