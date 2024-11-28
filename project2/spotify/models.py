from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .credentials import *

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.IntegerField(default=60)
    token_type = models.CharField(max_length=50)






