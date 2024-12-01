from .models import SpotifyToken
from django.utils import timezone

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    # Calculate the expiration time in seconds from now
    expires_in_seconds = timezone.now().timestamp() + expires_in

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