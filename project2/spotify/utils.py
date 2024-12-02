from .models import SpotifyToken
from django.utils import timezone

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    """
    Updates or creates a SpotifyToken for a user.

    This function checks if a SpotifyToken already exists for the given `session_id`.
    - If it exists, it updates the token with the new data.
    - If it doesn't exist, it creates a new token record.

    Args:
        session_id (str): The unique identifier for the user/session.
        access_token (str): The new access token for Spotify API access.
        token_type (str): The type of token (e.g., "Bearer").
        expires_in (int): Time (in seconds) until the token expires.
        refresh_token (str): The token used to refresh the access token.

    Returns:
        None
    """
    # Calculate the expiration time in seconds from now
    expires_in_seconds = timezone.now().timestamp() + expires_in

    # Check if a token already exists for the user
    tokens = SpotifyToken.objects.filter(user=session_id)
    if tokens.exists():
        # Update the existing token
        tokens = tokens.first()
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in_seconds  # Store as seconds
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        # Create a new token if one doesn't exist
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in_seconds,  # Store as seconds
            token_type=token_type
        )
        tokens.save()
