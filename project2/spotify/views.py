import spotipy
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserSpotifyLink
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from requests import Request, post
from django.conf import settings
from .utils import update_or_create_user_tokens

@csrf_protect
def login_and_connect_spotify(request):
    """
    Handles user login and initiates the Spotify authentication flow.

    If the user is successfully authenticated, it redirects them to the Spotify authorization URL.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to Spotify auth URL or renders the login page with an error.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            scopes = (
                'user-read-playback-state user-modify-playback-state '
                'user-read-currently-playing user-read-private user-top-read user-library-read'
            )
            url = Request(
                'GET',
                'https://accounts.spotify.com/authorize',
                params={
                    'scope': scopes,
                    'response_type': 'code',
                    'redirect_uri': settings.SPOTIPY_REDIRECT_URI,
                    'client_id': settings.SPOTIPY_CLIENT_ID,
                    'show_dialog': True
                }
            ).prepare().url
            return HttpResponseRedirect(url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('frontend:login')
    return render(request, 'frontend/login.html')


class AuthURL(APIView):
    """
    Returns the Spotify authorization URL with required scopes for the application.

    Methods:
        get: Handles GET requests to generate and return the Spotify authorization URL.
    """
    def get(self, request, format=None):
        scopes = (
            'user-read-playback-state user-modify-playback-state '
            'user-read-currently-playing user-read-private user-top-read user-library-read'
        )
        url = Request(
            'GET',
            'https://accounts.spotify.com/authorize',
            params={
                'scope': scopes,
                'response_type': 'code',
                'redirect_uri': settings.SPOTIPY_REDIRECT_URI,
                'client_id': settings.SPOTIPY_CLIENT_ID
            }
        ).prepare().url
        return Response({'url': url}, status=200)


def spotify_callback(request):
    """
    Handles Spotify's authorization callback, exchanging the auth code for tokens.

    Links the Spotify account to the authenticated user or updates existing tokens.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect: Redirects to the dashboard or login page based on success or error.
    """
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        messages.error(request, f"Spotify authorization failed: {error}")
        return redirect('frontend:login')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIPY_REDIRECT_URI,
        'client_id': settings.SPOTIPY_CLIENT_ID,
        'client_secret': settings.SPOTIPY_CLIENT_SECRET
    })

    response_data = response.json()
    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')
    refresh_token = response_data.get('refresh_token')
    expires_in = response_data.get('expires_in')

    if not access_token:
        messages.error(request, "Failed to obtain access token. Please try again.")
        return redirect('frontend:login')

    try:
        sp = spotipy.Spotify(auth=access_token)
        spotify_user_id = sp.current_user()['id']
        existing_link = UserSpotifyLink.objects.filter(spotify_user_id=spotify_user_id).first()

        if existing_link:
            if existing_link.user == request.user:
                messages.success(request, "Spotify account successfully linked!")
            else:
                messages.error(request, "This Spotify account is linked to another user.")
                return redirect('frontend:logout')

        UserSpotifyLink.objects.create(user=request.user, spotify_user_id=spotify_user_id)
        update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
        return redirect('wraps:dashboard')

    except spotipy.SpotifyException as e:
        messages.error(request, f"Spotify error: {str(e)}")
    except Exception as e:
        messages.error(request, f"Unexpected error: {str(e)}")
    return redirect('frontend:login')


def delete_account_view(request):
    """
    Handles account deletion for authenticated users.

    Deletes the user's account and logs them out of the application.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to dashboard or renders a logout template.
    """
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return render(request, 'frontend/spotify_logout.html')
    return redirect('frontend:dashboard')
