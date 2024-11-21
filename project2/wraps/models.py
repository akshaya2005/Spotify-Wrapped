from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserWrap(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(UserWrap, on_delete=models.CASCADE)
