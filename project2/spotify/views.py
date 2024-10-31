from django.shortcuts import render, redirect
from .credentials import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from .utils import *


# Create your views here.
class AuthURL(APIView):
    #returns the API endpoint that allows us to authenticate
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing' #find in spotify docs
        #creates a url for us
        url = Request('GET', 'https://accounts.spotify.com/authorize',
        params={'scope': scopes, 'response_type':'code', 'redirect_uri': SPOTIPY_REDIRECT_URI, 'client_id':SPOTIPY_CLIENT_ID}).prepare().url

        return Response({'url': url}, status = 200)


def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Handle error if exists
    if error:
        return redirect('frontend:index')  # Redirect to the index or an error page

    # Exchange the authorization code for an access token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    }).json()

    # Extract tokens and expiration info
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = int(response.get('expires_in'))

    # Ensure expires_in is a valid integer
    if expires_in is None:
        return redirect('frontend:index')  # Handle the case where expires_in is missing

    try:
        expires_in = int(expires_in)  # Convert to integer
    except ValueError:
        print("Error: 'expires_in' is not an integer:", expires_in)
        return redirect('frontend:index')  # Handle the error accordingly

    # Create session if it doesn't exist
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Update or create user tokens in the database
    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    # Redirect to the intro page after successful login
    return redirect('frontend:intro')  # Change this to match your intro page URL name


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status = status.HTTP_200_OK)
