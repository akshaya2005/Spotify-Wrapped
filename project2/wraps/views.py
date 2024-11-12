import spotipy
from django.shortcuts import render
from .models import *
import spotify
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .spotify_service import get_user_spotify_data

# Create your views here.

#@login_required  # Ensures only authenticated users can access this view
from django.shortcuts import redirect


def dashboard(request):
    # Get the current session ID
    session_id = request.session.session_key
    if not session_id:
        return redirect('frontend:index')  # Redirect if session doesn't exist

    # Retrieve the token for the current session
    token = spotify.models.SpotifyToken.objects.filter(user=session_id).first()

    # If no token is found, redirect to login
    if not token or not token.access_token:
        return redirect('frontend:index')  # Or your login page

    # Use the access token to get data from Spotify
    access_token = token.access_token
    spotify_data = get_user_spotify_data(access_token)  # Use this token to call Spotify API
    #print(spotify_data)
    if spotify_data:
        wrap_data = process_wrap_data(spotify_data)
        print(wrap_data)
        return render(request, 'frontend/dashboard.html', {'wrap_data': wrap_data})

    return render(request, 'frontend/dashboard.html', {'wrap_data': None})  # In case of no data

## Write functions to create different kinds of wraps

def create_wrap(request):
    user = request.user
    access_token = user.access_token  # Assuming you store access token in user model

    # Call the service function to get Spotify data
    spotify_data = get_user_spotify_data(access_token)
    print(spotify_data)
    if spotify_data:

        # Process the data into a wrap format (e.g., filter, sort, and format as needed)
        wrap_data = process_wrap_data(spotify_data)
        #print(wrap_data)
        return render(request, 'frontend/dashboard.html', {'wrap_data': wrap_data})
    else:
        # Handle error if data fetching failed
        return render(request, 'error.html', {'error': 'Failed to fetch Spotify data.'})

def create_top_artists_wrap():
    pass

def create_halloween_wrap():
    pass

def create_christmas_wrap():
    pass


def process_wrap_data(spotify_data):
    # Customize how you format data into wraps
    wraps = []
    for item in spotify_data['top_tracks']:
        wrap = {
            'title': item['name'],
            'content': item['artists'],

            # Add any other fields you want to display in the wrap
        }
        wraps.append(wrap)
    return wraps