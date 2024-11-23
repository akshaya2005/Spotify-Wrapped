from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class UserWrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    wrap_type = models.CharField(max_length=100)  # Type of wrap (e.g., 'top_tracks', 'top_artists')
    wrap_data = models.JSONField()  # Store wrap data as a JSON object
    created_at = models.DateTimeField(default=now)  # Timestamp for when the wrap was created

    def __str__(self):
        return f"{self.user.username}'s {self.wrap_type} wrap"


