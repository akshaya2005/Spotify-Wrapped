from django.apps import AppConfig


class WrapsConfig(AppConfig):
    """
    Configuration class for the 'wraps' application.

    This class defines the app's metadata and default settings.
    Attributes:
        default_auto_field (str): Specifies the default type for primary keys in models.
        name (str): The name of the application, corresponds to its directory name.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField for primary keys by default
    name = 'wraps'  # Name of the app, matching the directory structure
