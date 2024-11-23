import spotify
from django.shortcuts import render
from .spotify_service import *
from django.http import JsonResponse
from .models import *
# Create your views here.

#@login_required  # Ensures only authenticated users can access this view
from django.shortcuts import redirect


def dashboard(request):
    # Ensure the session exists
    session_id = request.session.session_key
    if not session_id:
        return redirect('frontend:login')  # Redirect to login if no session

    # Retrieve the token for the current session
    token = spotify.models.SpotifyToken.objects.filter(user=session_id).first()

    if not token or not token.access_token:
        return redirect('frontend:login')  # Redirect if no valid token

    # Get the access token
    access_token = token.access_token

    # Check if this is a POST request to generate a specific wrap
    if request.method == 'POST':
        wrap_type = request.POST.get('wrapTypeDropdown')

        try:
            # Generate the requested wrap
            if wrap_type == 'top_tracks':
                wrap_data = (get_user_top_tracks(access_token))
            elif wrap_type == 'top_artists':
                wrap_data = (get_user_top_artists(access_token))
            # elif wrap_type == 'top_albums':
            #     wrap_data = get_user_top_albums(access_token)
            # elif wrap_type == 'top_genres':
            #     wrap_data = get_user_top_genres(access_token)
            # elif wrap_type == 'top_playlists':
            #     wrap_data = get_user_top_playlists(access_token)
            else:
                wrap_data = {'error': 'Invalid wrap type selected'}

            user_wrap = UserWrap.objects.create(
                user=request.user,  # Save the user object
                wrap_type=wrap_type,  # Save the wrap type (e.g., 'top_tracks')
                wrap_data=wrap_data,  # Save the actual data (JSON or text)
            )

            # Return wrap data to the dashboard


        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    user_wraps = UserWrap.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'frontend/dashboard.html', {'wrap_data': user_wraps})

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