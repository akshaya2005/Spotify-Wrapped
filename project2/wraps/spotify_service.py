# yourapp/spotify_service.py

import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth


import spotipy

def get_user_spotify_data(access_token):
    print("get_user_spotify_data called")

    # Initialize the Spotipy client with the provided access token
    sp = spotipy.Spotify(auth=access_token)

    # Fetch the current user's profile information
    user_profile = sp.current_user()
    name = user_profile.get("display_name", "Unknown User")
    print("User Name:", name)

    # Fetch the user's top 10 tracks
    top_tracks_response = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    top_tracks = [
        {
            "name": track["name"],
            "artists": ", ".join([artist["name"] for artist in track["artists"]]),
            "album": track["album"]["name"],
            "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            "preview_url": track["preview_url"],
            "popularity": track["popularity"],
        }
        for track in top_tracks_response["items"]
    ]

    # Combine user profile and top tracks data in a dictionary to return
    spotify_data = {
        "user_name": name,
        "top_tracks": top_tracks,
    }

    return spotify_data
