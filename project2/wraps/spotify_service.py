# yourapp/spotify_service.py
import spotipy

def get_user_top_tracks(access_token):


    # Initialize the Spotipy client with the provided access token
    sp = spotipy.Spotify(auth=access_token)

    # Fetch the current user's profile information
    user_profile = sp.current_user()
    name = user_profile.get("display_name", "Unknown User")


    # Fetch the user's top 10 tracks
    top_tracks_response = sp.current_user_top_tracks(limit=5, time_range='medium_term')
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
        "name" : "Top Tracks",
        "content": top_tracks,
    }

    return spotify_data

def get_user_top_artists(access_token):
    # Initialize Spotify client
    sp = spotipy.Spotify(auth=access_token)

    # Fetch the current user's profile information



    # Fetch the user's top 5 artists
    try:
        top_artists_response = sp.current_user_top_artists(limit=5, time_range='medium_term')


        top_artists = [
            {"artist_name": artist["name"],
             "popularity": artist["popularity"],
             "genres": artist["genres"]}
            for artist in top_artists_response["items"]
        ]
        spotify_data = {"name": "Top Artists", "content" :top_artists}
        return spotify_data
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top artists: {e}")

def get_christmas_wrap(access_token):
    pass



