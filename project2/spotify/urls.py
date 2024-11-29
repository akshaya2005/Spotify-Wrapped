from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, login_and_connect_spotify, spotify_logout

app_name = 'spotify'  # Add this to name the app, which can be helpful for namespacing

urlpatterns = [
    path('get-auth-url/', AuthURL.as_view(), name='get_auth_url'),  # Ensure this matches
    path('redirect/', spotify_callback, name='callback'),
    path('is-authenticated/', IsAuthenticated.as_view(), name='is_authenticated'),
    path('login/', login_and_connect_spotify, name='login_and_connect_spotify'),
    path('spotify/logout/', spotify_logout, name='spotify_logout'),
]
