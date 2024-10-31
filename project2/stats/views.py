from django.shortcuts import render, redirect
import spotipy
from django.contrib.auth.decorators import login_required


@login_required
def stats_view(request):
    token_info = request.session.get('token_info')

    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Fetch user's top artists and top tracks
        top_artists = sp.current_user_top_artists(limit=10)['items']
        top_tracks = sp.current_user_top_tracks(limit=10)['items']

        return render(request, 'stats.html', {
            'top_artists': top_artists,
            'top_tracks': top_tracks,
        })

    return redirect('login')  # Redirect to login if token_info is not present
