import spotify
import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .spotify_service import *
from .models import UserWrap


def dashboard(request):
    """
    Displays the user's dashboard with saved wraps or allows generating new wraps.

    This view checks if the user's Spotify account is linked and if a valid session exists.
    Users can generate new wraps by selecting options from the dashboard, which
    are saved to the database for future access.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered dashboard template or a redirect to login/Spotify linking.
    """
    # Ensure the user has linked their Spotify account
    if not hasattr(request.user, 'userspotifylink'):
        messages.error(request, "Please link your Spotify account to proceed.")
        return redirect('spotify:login_and_connect_spotify')

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

    # Handle POST request for generating wraps
    if request.method == 'POST':
        wrap_name = ""
        wrap_type = request.POST.get('wrapTypeDropdown')
        time_period = request.POST.get("time_period")

        try:
            # Generate the requested wrap
            if wrap_type == 'top_tracks':
                wrap_name = 'Top Tracks'
                wrap_data = get_user_top_tracks(access_token, time_range=time_period)
            elif wrap_type == 'top_artists':
                wrap_name = 'Top Artists'
                wrap_data = get_user_top_artists(access_token, time_range=time_period)
            elif wrap_type == 'top_albums':
                wrap_name = 'Top Albums'
                wrap_data = get_user_top_albums(access_token, time_range=time_period)
            elif wrap_type == 'top_genres':
                wrap_name = 'Top Genres'
                wrap_data = get_user_top_genres(access_token, time_range=time_period)
            elif wrap_type == 'top_playlists':
                wrap_name = 'Top Playlists'
                wrap_data = get_user_top_playlists(access_token)
            else:
                wrap_data = {'error': 'Invalid wrap type selected'}

            # Save the generated wrap to the database
            user_wrap = UserWrap.objects.create(
                user=request.user,
                wrap_name=wrap_name,
                wrap_type=wrap_type,
                wrap_data=wrap_data,
            )

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Fetch and serialize user wraps for display
    user_wraps = UserWrap.objects.filter(user=request.user).order_by('-created_at')
    wraps_with_serialized_data = [
        {
            "id": wrap.id,
            "wrap_name": wrap.wrap_name,
            "wrap_type": wrap.wrap_type,
            "wrap_data": json.dumps(wrap.wrap_data),  # Convert to valid JSON
            "created_at": wrap.created_at,
        }
        for wrap in user_wraps
    ]

    return render(request, 'frontend/dashboard.html', {'wrap_data': wraps_with_serialized_data})


def delete_wrap(request, wrap_id):
    """
    Deletes a specific wrap for the logged-in user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        wrap_id (int): The ID of the wrap to be deleted.

    Returns:
        HttpResponse: Redirect to the dashboard on success or an error response for invalid methods.
    """
    if request.method == 'POST':
        # Get the wrap instance for the logged-in user
        wrap = get_object_or_404(UserWrap, id=wrap_id, user=request.user)
        wrap.delete()  # Delete the wrap
        return redirect('wraps:dashboard')  # Redirect to the dashboard after deletion

    return HttpResponse("Invalid request method", status=405)
