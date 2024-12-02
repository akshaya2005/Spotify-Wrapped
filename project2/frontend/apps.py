from django.apps import AppConfig

class FrontendConfig(AppConfig):
    """
    Configuration class for the 'frontend' application.

    Attributes:
        default_auto_field (str): Specifies the default type for primary keys
                                  in models if not explicitly defined.
        name (str): The name of the application, corresponds to its folder name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frontend'