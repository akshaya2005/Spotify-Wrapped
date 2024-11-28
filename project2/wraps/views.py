import spotify
import json
from django.shortcuts import render
from .spotify_service import *
from django.http import JsonResponse
from .models import *
# Create your views here.

#@login_required  # Ensures only authenticated users can access this view
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse




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
            elif wrap_type == 'top_albums':
                wrap_data = get_user_top_albums(access_token)
            elif wrap_type == 'top_genres':
                wrap_data = get_user_top_genres(access_token)
            elif wrap_type == 'top_playlists':
                wrap_data = get_user_top_playlists(access_token)
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
    wraps_with_serialized_data = [
        {
            "id": wrap.id,
            "wrap_type": wrap.wrap_type,
            "wrap_data": json.dumps(wrap.wrap_data),  # Convert to valid JSON
            "created_at": wrap.created_at,
        }
        for wrap in user_wraps
    ]

    return render(request, 'frontend/dashboard.html', {'wrap_data': wraps_with_serialized_data})
    #return render(request, 'frontend/dashboard.html', {'wrap_data': user_wraps})

def delete_wrap(request, wrap_id):
    if request.method == 'POST':
        # Get the wrap instance for the logged-in user
        wrap = get_object_or_404(UserWrap, id=wrap_id, user=request.user)
        wrap.delete()  # Delete the wrap
        return redirect('wraps:dashboard')  # Redirect to the dashboard after deletion
    return HttpResponse("Invalid request method", status=405)




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