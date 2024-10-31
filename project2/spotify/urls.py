from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated

app_name = 'spotify'  # Add this to name the app, which can be helpful for namespacing

urlpatterns = [
    path('get-auth-url/', AuthURL.as_view(), name='get_auth_url'),  # Ensure this matches
    path('redirect/', spotify_callback, name='callback'),
    path('is-authenticated/', IsAuthenticated.as_view(), name='is_authenticated')
]
