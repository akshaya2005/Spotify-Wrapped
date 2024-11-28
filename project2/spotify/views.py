from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from requests import Request
from .credentials import SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
import datetime
import requests  # For making API requests to Spotify
from django.shortcuts import redirect


# Create your views here.
def get_auth_url(request):
    scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-top-read'
    url = Request(
        'GET',
        'https://accounts.spotify.com/authorize',
        params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': SPOTIPY_REDIRECT_URI,
            'client_id': SPOTIPY_CLIENT_ID,
        }
    ).prepare().url

    return HttpResponseRedirect(url)

@csrf_protect
def login_and_connect_spotify(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-top-read'
            url = Request(
                'GET',
                'https://accounts.spotify.com/authorize',
                params={
                    'scope': scopes,
                    'response_type': 'code',
                    'redirect_uri': SPOTIPY_REDIRECT_URI,
                    'client_id': SPOTIPY_CLIENT_ID
                }
            ).prepare().url

            return HttpResponseRedirect(url)
        else:
            # Show an error message if authentication failed
            return render(request, 'frontend/login.html', {'error': 'Invalid username or password.'})

    # Render the login page if the request is not POST
    return render(request, 'frontend/login.html')



class AuthURL(APIView):
    #returns the API endpoint that allows us to authenticate
    def get(self, request, format=None):
        scopes = 'user-read-private user-top-read'
        url = Request('GET', 'https://accounts.spotify.com/authorize',
        params={'scope': scopes, 'response_type':'code', 'redirect_uri': SPOTIPY_REDIRECT_URI, 'client_id':SPOTIPY_CLIENT_ID}).prepare().url

        return Response({'url': url}, status = 200)



def spotify_callback(request):
    # print("Received response:")  # Logs response from Spotify
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Handle error if exists
    if error:
        print("Error in Spotify callback:", error)  # Log the error for debugging
        return redirect('frontend:login')  # Redirect to the index or an error page

    # Exchange the authorization code for an access token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    })

    # Extract tokens and expiration info
    response_data = response.json()
    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')
    refresh_token = response_data.get('refresh_token')
    expires_in = response_data.get('expires_in')

    # Ensure expires_in is a valid integer
    if expires_in is None or not isinstance(expires_in, int):
        print("Error: 'expires_in' is missing or not an integer:", expires_in)
        return redirect('frontend:index')  # Handle the case where expires_in is missing

    # Create session if it doesn't exist
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    # Save access token and link the Spotify user ID with the authenticated Django user


    # Redirect to the intro page after successful login
    return redirect('wraps:dashboard')  # Change this to match your intro page URL name

# def spotify_callback(request):
#     code = request.GET.get('code')
#     error = request.GET.get('error')
#
#     # Handle error if exists
#     if error:
#         print("Error in Spotify callback:", error)  # Log the error for debugging
#         return redirect('frontend:login')  # Redirect to the index or an error page
#
#     # Exchange the authorization code for an access token
#     response = post('https://accounts.spotify.com/api/token', data={
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': SPOTIPY_REDIRECT_URI,
#         'client_id': SPOTIPY_CLIENT_ID,
#         'client_secret': SPOTIPY_CLIENT_SECRET
#     })
#
#     # Extract tokens and expiration info
#     response_data = response.json()
#     access_token = response_data.get('access_token')
#     token_type = response_data.get('token_type')
#     refresh_token = response_data.get('refresh_token')
#     expires_in = response_data.get('expires_in')
#
#     # Ensure expires_in is a valid integer
#     if expires_in is None or not isinstance(expires_in, int):
#         print("Error: 'expires_in' is missing or not an integer:", expires_in)
#         return redirect('frontend:index')  # Handle the case where expires_in is missing
#
#     # Check if the user is authenticated (i.e., logged in)
#     user = request.user
#     if user.is_authenticated:
#         # Check if the user already has a linked Spotify account
#         spotify_account = SpotifyToken.objects.filter(user=user).first()
#         if spotify_account:
#             # If a Spotify account is already linked, update the token details
#             spotify_account.access_token = access_token
#             spotify_account.refresh_token = refresh_token
#             spotify_account.token_expiration = timezone.now() + datetime.timedelta(seconds=expires_in)
#             spotify_account.token_type = token_type
#             spotify_account.save()
#         else:
#             # If no Spotify account is linked, create a new SpotifyToken record
#             spotify_account = SpotifyToken(
#                 user=user,  # Link this Spotify account to the logged-in user
#                 access_token=access_token,
#                 refresh_token=refresh_token,
#                 token_expiration=timezone.now() + datetime.timedelta(seconds=expires_in),
#                 token_type=token_type
#             )
#             spotify_account.save()
#
#         return redirect('wraps:dashboard')  # Redirect to the dashboard or a page after successful linking
#     else:
#         # If the user is not logged in, redirect them to the login page
#         return redirect('frontend:login')






class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status = status.HTTP_200_OK)
