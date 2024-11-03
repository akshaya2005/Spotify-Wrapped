from .models import SpotifyToken
from django.utils import timezone
from .credentials import *
from requests import post

def get_user_tokens(session_id):
    try:
        # Fetch the user's tokens
        user_tokens = SpotifyToken.objects.get(user=session_id)
        return user_tokens  # Return the token object
    except SpotifyToken.DoesNotExist:
        return None  # Return None if no tokens found


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = SpotifyToken.objects.get(user=session_id)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token,
                              expires_in=expires_in)
        tokens.save()  # Saves it to the database



def is_spotify_authenticated(session_id):
    tokens = SpotifyToken.objects.get(user=session_id)
    if tokens:
        expiry_time = tokens.created_at.timestamp() + tokens.expires_in  # Calculate the actual expiration timestamp
        if expiry_time <= timezone.now().timestamp():
            refresh_spotify_token(session_id)
        return True
    return False


def refresh_spotify_token(session_id):
    refresh_token = SpotifyToken.objects.get(user=session_id).refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    }).json()

    print("Response from Spotify:", response)

    access_token = response.get('access_token')
    token_type = response.get('token_type')

    # Check for 'expires_in' before trying to convert
    expires_in = int(response.get('expires_in'))  # Duration in seconds
    if expires_in is not None:
        try:
            expires_in = int(expires_in)  # Ensure it's an integer
        except ValueError:
            print("Error: 'expires_in' is not an integer:", expires_in)
            return  # Handle error accordingly, possibly return to prevent further errors

    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

