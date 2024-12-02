from django.apps import AppConfig


class SpotifyConfig(AppConfig):
    """
    Configuration class for the 'spotify' Django application.

    This class defines application-specific settings and metadata for the 'spotify' app.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key for models
            in this application. Defaults to 'django.db.models.BigAutoField'.
        name (str): The full Python path to the application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spotify'
