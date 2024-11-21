import spotipy
from django.shortcuts import render
from .models import *
import spotify
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .spotify_service import *

# Create your views here.

#@login_required  # Ensures only authenticated users can access this view
from django.shortcuts import redirect


def dashboard(request):
    # Get the current session ID
    session_id = request.session.session_key
    if not session_id:
        return redirect('frontend:login')  # Redirect if session doesn't exist

    # Retrieve the token for the current session
    token = spotify.models.SpotifyToken.objects.filter(user=session_id).first()

    # If no token is found, redirect to login
    if not token or not token.access_token:
        return redirect('frontend:login')  # Or your login page

    # Use the access token to get data from Spotify
    access_token = token.access_token
    # use methods from spotify_service to retrieve the data to put into the wraps
    top_tracks = get_user_top_tracks(access_token)  # returns a dictionary with the name of the wrap and content
    top_artists = get_user_top_artists(access_token)
    print(top_artists)
    # if spotify_data:
    #     wrap_data = process_wrap_data(spotify_data)
    #     print(wrap_data)
    #     return render(request, 'frontend/dashboard.html', {'wrap_data': wrap_data})
    #
    # return render(request, 'frontend/dashboard.html', {'wrap_data': None})  # In case of no data
    # create an array contaning all the wraps
    wrap_data = [
        top_tracks,
        top_artists,
    ]
    return render(request, 'frontend/dashboard.html', {'wrap_data': wrap_data})

## Write functions to create different kinds of wraps
def toggle_favorite(request, place_id):
    # Get or create the restaurant based on place_id
    # restaurant, created = Restaurants.objects.get_or_create(place_id=place_id, defaults={
    #     'name': request.POST.get('name'),
    #     'address': request.POST.get('address'),
    #     'latitude': request.POST.get('latitude'),
    #     'longitude': request.POST.get('longitude'),
    # })
    #
    # # Check if the restaurant is already in the user's favorites
    # favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()
    #
    # if favorite:
    #     # If it is already a favorite, remove it
    #     favorite.delete()
    #     message = "Removed from favorites"
    # else:
    #     # Otherwise, add it to favorites
    #     Favorite.objects.create(user=request.user, restaurant=restaurant)
    #     message = "Added to favorites"
    #
    # return JsonResponse({'message': message})
    pass


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