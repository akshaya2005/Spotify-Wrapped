"""
URL configuration for the 'spotify' application.

This module defines the URL patterns for the Spotify-related features of the project,
such as authentication, callbacks, and account deletion.

App Name:
    spotify: This app name is used for namespacing in templates and reverse URL lookups.

URL Patterns:
    - /get-auth-url/: Generates the Spotify authorization URL.
    - /redirect/: Handles the Spotify authentication callback.
    - /login/: Logs in the user and connects their Spotify account.
    - /delete-account/: Allows the user to delete their Spotify-related data.
"""

from django.urls import path
from .views import AuthURL, spotify_callback, login_and_connect_spotify, delete_account_view

# App namespace for referencing URLs in templates and views
app_name = 'spotify'

urlpatterns = [
    path('get-auth-url/', AuthURL.as_view(), name='get_auth_url'),  # Generate Spotify authorization URL
    path('redirect/', spotify_callback, name='callback'),  # Handle Spotify callback
    path('login/', login_and_connect_spotify, name='login_and_connect_spotify'),  # Login and connect Spotify
    path('delete-account/', delete_account_view, name='delete_account'),  # Delete user account and data
]
