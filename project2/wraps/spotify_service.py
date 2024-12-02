import spotipy

def get_user_top_tracks(access_token, time_range):
    """
    Fetches the user's top tracks from Spotify.

    Args:
        access_token (str): The access token for Spotify API.
        time_range (str): The time range for fetching top tracks ('short_term', 'medium_term', 'long_term').

    Returns:
        dict: Contains the user's top tracks with metadata (name, artists, album, etc.).
    """
    sp = spotipy.Spotify(auth=access_token)
    try:
        top_tracks_response = sp.current_user_top_tracks(limit=5, time_range=time_range)
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
        top_tracks_sorted = top_tracks[::-1]  # Reverse order for ascending popularity
        return {"name": "Top Tracks", "content": top_tracks_sorted}
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top tracks: {e}")


def get_user_top_artists(access_token, time_range):
    """
    Fetches the user's top artists from Spotify.

    Args:
        access_token (str): The access token for Spotify API.
        time_range (str): The time range for fetching top artists ('short_term', 'medium_term', 'long_term').

    Returns:
        dict: Contains the user's top artists with metadata (name, popularity, genres, etc.).
    """
    sp = spotipy.Spotify(auth=access_token)
    try:
        top_artists_response = sp.current_user_top_artists(limit=5, time_range=time_range)
        top_artists = [
            {
                "artist_name": artist["name"],
                "popularity": artist["popularity"],
                "genres": artist["genres"],
                "profile_picture": artist["images"][0]["url"] if artist["images"] else None,
            }
            for artist in top_artists_response["items"]
        ]
        top_artists_sorted = top_artists[::-1]
        return {"name": "Top Artists", "content": top_artists_sorted}
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top artists: {e}")


def get_user_top_albums(access_token, time_range):
    """
    Fetches the user's top albums derived from their top tracks.

    Args:
        access_token (str): The access token for Spotify API.
        time_range (str): The time range for fetching top tracks ('short_term', 'medium_term', 'long_term').

    Returns:
        dict: Contains the user's top albums with metadata (name, artists, release date, etc.).
    """
    import collections
    sp = spotipy.Spotify(auth=access_token)
    try:
        top_tracks_response = sp.current_user_top_tracks(limit=50, time_range=time_range)
        album_popularity = collections.defaultdict(list)

        for track in top_tracks_response["items"]:
            album = track["album"]
            album_id = album["id"]
            album_popularity[album_id].append(track["popularity"])

        sorted_albums = sorted(
            album_popularity.items(),
            key=lambda x: sum(x[1]) / len(x[1]),
            reverse=True
        )
        top_albums = []
        for album_id, popularity_scores in sorted_albums[:5]:
            album = sp.album(album_id)
            top_albums.append({
                "name": album["name"],
                "artists": [artist["name"] for artist in album["artists"]],
                "release_date": album["release_date"],
                "album_cover": album["images"][0]["url"] if album["images"] else None,
                "total_tracks": album["total_tracks"],
                "average_popularity": sum(popularity_scores) / len(popularity_scores),
            })
        return {"name": "Top Albums", "content": top_albums[::-1]}
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top albums: {e}")
        if e.http_status == 403:
            raise Exception("Insufficient client scope. Please ensure 'user-top-read' is granted.")


def get_user_top_genres(access_token, time_range):
    """
    Fetches the user's top genres derived from their top artists.

    Args:
        access_token (str): The access token for Spotify API.
        time_range (str): The time range for fetching top artists ('short_term', 'medium_term', 'long_term').

    Returns:
        dict: Contains the user's top genres with counts.
    """
    sp = spotipy.Spotify(auth=access_token)
    try:
        top_artists_response = sp.current_user_top_artists(limit=50, time_range=time_range)
        genre_counts = {}
        for artist in top_artists_response["items"]:
            for genre in artist["genres"]:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        top_genres = [{"genre": genre, "count": count} for genre, count in sorted_genres[:5]]
        return {"name": "Top Genres", "content": top_genres[::-1]}
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top genres: {e}")


def get_user_top_playlists(access_token):
    """
    Fetches the user's top playlists from Spotify.

    Args:
        access_token (str): The access token for Spotify API.

    Returns:
        dict: Contains the user's top playlists with metadata (name, description, owner, etc.).
    """
    sp = spotipy.Spotify(auth=access_token)
    try:
        playlists_response = sp.current_user_playlists(limit=5)
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
        return {"name": "Top Playlists", "content": top_playlists}
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top playlists: {e}")
