from django.db import models
from django.contrib.auth.models import User

class SpotifyToken(models.Model):
    """
    Represents an OAuth token for interacting with Spotify's API.

    Attributes:
        user (str): The username or unique identifier associated with the token.
        created_at (datetime): Timestamp when the token was created.
        refresh_token (str): Token used to refresh the access token.
        access_token (str): Token used to access Spotify's API.
        expires_in (int): Time in seconds until the token expires.
        token_type (str): The type of token, typically "Bearer".
    """
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.IntegerField(default=60)
    token_type = models.CharField(max_length=50)

    def __str__(self):
        """
        Returns a string representation of the SpotifyToken object.

        Returns:
            str: A representation showing the user and token type.
        """
        return f"{self.user} - {self.token_type}"


class UserSpotifyLink(models.Model):
    """
    Links a Django user to their Spotify account.

    Attributes:
        user (User): A one-to-one relationship with Django's built-in User model.
        spotify_user_id (str): The unique identifier for the Spotify user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_user_id = models.CharField(max_length=255, unique=True)  # Spotify user ID

    def __str__(self):
        """
        Returns a string representation of the UserSpotifyLink object.

        Returns:
            str: A representation showing the username and Spotify user ID.
        """
        return f"{self.user.username} - {self.spotify_user_id}"
