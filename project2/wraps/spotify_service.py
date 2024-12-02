# yourapp/spotify_service.py
import spotipy

def get_user_top_tracks(access_token, time_range):
    # Initialize the Spotipy client with the provided access token
    sp = spotipy.Spotify(auth=access_token)
    try:
        top_tracks_response = sp.current_user_top_tracks(limit=8, time_range=time_range)
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
        print(top_tracks_response["items"][0])

        # Sort the artists by popularity in ascending order (5th most to 1st)
        top_tracks_sorted = top_tracks[::-1]

        # Combine user profile and top tracks data in a dictionary to return
        spotify_data = {
            "name" : "Top Tracks",
            "content": top_tracks_sorted,
        }
        return spotify_data

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top tracks: {e}")

def get_user_top_artists(access_token, time_range):
    # Initialize Spotify client
    sp = spotipy.Spotify(auth=access_token)
    # Fetch the user's top 5 artists
    try:
        top_artists_response = sp.current_user_top_artists(limit=8, time_range=time_range)
        top_artists = [
            {
                "artist_name": artist["name"],
                "popularity": artist["popularity"],
                "genres": artist["genres"],
                "profile_picture": artist["images"][0]["url"] if artist["images"] else None,
             }
            for artist in top_artists_response["items"]
        ]

        # Sort the artists by popularity in ascending order (5th most to 1st)
        top_artists_sorted = top_artists[::-1]

        spotify_data = {"name": "Top Artists", "content" :top_artists_sorted}

        return spotify_data

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top artists: {e}")


def get_user_top_albums(access_token, time_range):
    import collections
    sp = spotipy.Spotify(auth=access_token)

    try:
        # Fetch the user's top tracks
        top_tracks_response = sp.current_user_top_tracks(limit=50, time_range=time_range)
        top_tracks = top_tracks_response["items"]

        # Extract album data from the top tracks
        album_popularity = collections.defaultdict(list)  # Tracks albums and their popularity scores
        for track in top_tracks:
            album = track["album"]
            album_id = album["id"]
            album_data = {
                "name": album["name"],
                "artists": ", ".join([artist["name"] for artist in album["artists"]]),
                "release_date": album["release_date"],
                "album_cover": album["images"][0]["url"] if album["images"] else None,
                "total_tracks": album["total_tracks"],
            }
            album_popularity[album_id].append(track["popularity"])
        # Calculate average popularity for each album
        sorted_albums = sorted(
            album_popularity.items(),
            key=lambda x: sum(x[1]) / len(x[1]),  # Average popularity
            reverse=True
        )
        #print(sorted_albums)
        # Prepare the top albums list
        top_albums = []
        for album_id, popularity_scores in sorted_albums[:8]:
            album = sp.album(album_id)
            album_data = {
                "name": album["name"],
                "artists": [artist["name"] for artist in album["artists"]],
                "release_date": album["release_date"],
                "album_cover": album["images"][0]["url"] if album["images"] else None,
                "total_tracks": album["total_tracks"],
                "average_popularity": sum(popularity_scores) / len(popularity_scores),
            }
            top_albums.append(album_data)

        # Sort the artists by popularity in ascending order (5th most to 1st)
        top_albums_sorted = top_albums[::-1]
        return {"name": "Top Albums", "content": top_albums_sorted}

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top albums: {e}")
        if e.http_status == 403:
            raise Exception("Insufficient client scope. Please ensure 'user-top-read' is granted.")
        return None


def get_user_top_genres(access_token, time_range):
    sp = spotipy.Spotify(auth=access_token)
    try:
        # Fetch the user's top artists to derive genres
        top_artists_response = sp.current_user_top_artists(limit=50, time_range=time_range)
        genre_counts = {}
        for artist in top_artists_response["items"]:
            for genre in artist["genres"]:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        # Sort genres by popularity
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        top_genres = [{"genre": genre, "count": count} for genre, count in sorted_genres[:5]]

        # Sort the artists by popularity in ascending order (5th most to 1st)
        top_genres_sorted = top_genres[::-1]
        spotify_data = {
            "name": "Top Genres",
            "content": top_genres_sorted,
        }
        return spotify_data
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top genres: {e}")


def get_user_top_playlists(access_token):
    sp = spotipy.Spotify(auth=access_token)
    try:
        # Fetch the user's playlists
        playlists_response = sp.current_user_playlists(limit=8)
        top_playlists = [
            {
                "name": playlist["name"],
                "description": playlist["description"],
                "owner": playlist["owner"]["display_name"],
                "tracks_count": playlist["tracks"]["total"],
                "playlist_cover": playlist["images"][0]["url"] if playlist["images"] else None,
            }
            for playlist in playlists_response["items"]
        ]

        top_playlists_sorted = top_playlists[::-1]

        spotify_data = {
            "name": "Top Playlists",
            "content": top_playlists_sorted,
        }
        return spotify_data
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top playlists: {e}")