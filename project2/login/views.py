from django.shortcuts import render, redirect
from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth
import spotipy

sp_oauth = SpotifyOAuth(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIFY_REDIRECT_URI,
    scope='user-top-read'
)

def login_view(request):
    if request.method == 'GET':
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    return render(request, 'login.html')

def callback_view(request):
    # Handle Spotify's callback, exchange code for token
    code = request.GET.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        request.session['token_info'] = token_info
        return redirect('stats:stats')  # Redirect to stats after successful login
    return redirect('login:login')  # If no code, restart login process
