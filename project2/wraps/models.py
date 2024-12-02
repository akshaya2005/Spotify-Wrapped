from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserWrap(models.Model):
    """
    Represents a user-generated wrap that stores data related to user preferences or activity.

    Attributes:
        user (ForeignKey): A relationship linking this wrap to a specific user.
        wrap_name (CharField): An optional name for the wrap (e.g., 'My Top Tracks').
        wrap_type (CharField): The type of the wrap (e.g., 'top_tracks', 'top_artists').
        wrap_data (JSONField): Stores the wrap's content as a JSON object.
        created_at (DateTimeField): Timestamp indicating when the wrap was created.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  # Deletes all associated wraps if the user is deleted.
    wrap_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )  # Wrap name is optional and can be left blank.
    wrap_type = models.CharField(
        max_length=100
    )  # Specifies the category or type of the wrap.
    wrap_data = models.JSONField()  # Stores wrap details in JSON format.
    created_at = models.DateTimeField(
        default=now
    )  # Automatically sets the creation time to the current time.

    def __str__(self):
        """
        Returns a human-readable representation of the UserWrap object.

        Returns:
            str: A string describing the user's wrap type.
        """
        return f"{self.user.username}'s {self.wrap_type} wrap"
