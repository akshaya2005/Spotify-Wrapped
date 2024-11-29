from .models import SpotifyToken
from .credentials import *
from requests import post

def get_user_tokens(session_id):
    try:
        # Fetch the user's tokens
        user_tokens = SpotifyToken.objects.get(user=session_id)
        return user_tokens  # Return the token object
    except SpotifyToken.DoesNotExist:
        return None  # Return None if no tokens found


from django.utils import timezone

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    # Calculate the expiration time in seconds from now
    expires_in_seconds = timezone.now().timestamp() + expires_in

    tokens = SpotifyToken.objects.filter(user=session_id)
    if tokens.exists():
        # Update the existing token
        tokens = tokens.first()
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in_seconds  # Store as seconds
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        # Create a new token if one doesn't exist
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in_seconds,  # Store as seconds
            token_type=token_type
        )
        tokens.save()




def is_spotify_authenticated(session_id):
    tokens = SpotifyToken.objects.filter(user=session_id)
    if tokens.exists():
        tokens = tokens.first()
        expiry_time = tokens.created_at.timestamp() + tokens.expires_in  # Calculate the actual expiration timestamp
        if expiry_time <= timezone.now().timestamp():
            refresh_spotify_token(session_id)
        return True
    return False



def refresh_spotify_token(session_id):
    tokens = SpotifyToken.objects.filter(user=session_id)
    if not tokens.exists():
        print("No token found for session_id:", session_id)
        return  # Exit if there’s no token to refresh

    refresh_token = tokens.first().refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    }).json()

    print("Response from Spotify:", response)

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    if expires_in is not None:
        try:
            expires_in = int(expires_in)
        except ValueError:
            print("Error: 'expires_in' is not an integer:", expires_in)
            return

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

import requests

def get_spotify_user_id_from_access_token(access_token):
    url = "https://api.spotify.com/v1/me"  # Endpoint to fetch the current user's profile
    headers = {
        "Authorization": f"Bearer {access_token}"  # Include the access token in the Authorization header
    }

    # Make the request to Spotify's API
    response = requests.get(url, headers=headers)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        user_data = response.json()
        spotify_user_id = user_data.get('id')  # Extract the Spotify user ID from the response
        return spotify_user_id
    else:
        # Handle the error (e.g., access token might have expired)
        print(f"Error fetching user data from Spotify: {response.status_code}")
        return None


