import spotipy
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import UserSpotifyLink
from .utils import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from requests import Request
from .credentials import SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from django.shortcuts import redirect
from requests import post
from .utils import update_or_create_user_tokens

# Create your views here.
@csrf_protect
def login_and_connect_spotify(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)

            # Define Spotify scopes
            scopes = (
                'user-read-playback-state user-modify-playback-state '
                'user-read-currently-playing user-read-private user-top-read user-library-read'
            )

            # Generate the Spotify authorization URL
            url = Request(
                'GET',
                'https://accounts.spotify.com/authorize',
                params={
                    'scope': scopes,
                    'response_type': 'code',
                    'redirect_uri': SPOTIPY_REDIRECT_URI,
                    'client_id': SPOTIPY_CLIENT_ID,
                    'show_dialog': True
                }
            ).prepare().url

            return HttpResponseRedirect(url)
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid username or password. Please check your credentials and try again.")
            return redirect('frontend:login')  # Redirect back to the login page

    # If the request is not POST, render the login page
    return render(request, 'frontend/login.html')


class AuthURL(APIView):
    #returns the API endpoint that allows us to authenticate
    def get(self, request, format=None):
        scopes = (
            'user-read-playback-state user-modify-playback-state '
            'user-read-currently-playing user-read-private user-top-read user-library-read'
        )
        url = Request('GET', 'https://accounts.spotify.com/authorize',
        params={'scope': scopes, 'response_type':'code', 'redirect_uri': SPOTIPY_REDIRECT_URI, 'client_id':SPOTIPY_CLIENT_ID}).prepare().url

        return Response({'url': url}, status = 200)


def spotify_callback(request):
    # Extract code and error from the Spotify redirect response
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        error_message = f"Spotify authorization failed: {error}"
        messages.error(request, error_message)
        return redirect('frontend:login')

    # Exchange authorization code for access token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    })

    # Parse the response
    response_data = response.json()
    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')
    refresh_token = response_data.get('refresh_token')
    expires_in = response_data.get('expires_in')

    # Ensure expires_in is a valid integer
    if expires_in is None or not isinstance(expires_in, int):
        print("Error: 'expires_in' is missing or not an integer:", expires_in)
        return redirect('frontend:login')  # Handle the case where expires_in is missing

    if not access_token:
        # Handle token exchange failure
        error_message = "Failed to obtain access token from Spotify. Please try again."
        messages.error(request, error_message)
        return redirect('frontend:login')

    try:
        # Use Spotipy to fetch the Spotify user ID
        sp = spotipy.Spotify(auth=access_token)
        spotify_user_id = sp.current_user()['id']

        # Check if Spotify account is already linked
        existing_link = UserSpotifyLink.objects.filter(spotify_user_id=spotify_user_id).first()

        if existing_link:
            if existing_link.user == request.user:
                # If the Spotify account is already linked to the current user, allow login
                messages.success(request, "Spotify account successfully linked!")
                # Create session if it doesn't exist
                if not request.session.exists(request.session.session_key):
                    request.session.create()
                update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in,
                                             refresh_token)
                return redirect('wraps:dashboard')  # Redirect to the user's dashboard
            else:
                # If the Spotify account is linked to a different user
                error_message = "This Spotify account is already linked to another user."
                # request.user.delete()
                messages.error(request, error_message)
                return redirect('frontend:logout')

        # Link the Spotify account to the current user if it's not already linked
        UserSpotifyLink.objects.create(user=request.user, spotify_user_id=spotify_user_id)
        messages.success(request, "Spotify account successfully linked!")
        # Create session if it doesn't exist
        if not request.session.exists(request.session.session_key):
            request.session.create()
        update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
        return redirect('wraps:dashboard')  # Redirect to the user's dashboard

    except spotipy.SpotifyException as e:
        # Handle Spotipy-specific errors
        error_message = f"An error occurred while linking your Spotify account: {str(e)}"
        messages.error(request, error_message)
        return redirect('frontend:login')

    except Exception as e:
        # Catch any other unexpected errors
        error_message = f"An unexpected error occurred: {str(e)}"
        messages.error(request, error_message)
        return redirect('frontend:login')

def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            # Delete the user's account
            user.delete()

            # Log out the user
            logout(request)

            # Add a success message (optional)
            messages.success(request, "Your account has been deleted successfully.")
            return render(request, 'frontend/spotify_logout.html')

    return redirect('frontend:dashboard')  # Prevent access via GET