from django.contrib import admin
from .models import UserSpotifyLink

# Register your models here.

"""
Admin configuration for the 'frontend' application.

This file is used to customize how models are managed and displayed 
in the Django admin interface.
"""

# Register the UserSpotifyLink model
admin.site.register(UserSpotifyLink)
"""
Registers the `UserSpotifyLink` model with the Django admin site.

This allows administrators to view, edit, and manage `UserSpotifyLink`
records through the admin interface.
"""
