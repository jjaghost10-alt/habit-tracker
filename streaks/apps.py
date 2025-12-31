from django.apps import AppConfig


class StreaksConfig(AppConfig):
    """
    Application configuration for the streaks app.

    This class registers the streaks application with Django
    and allows Django to identify the app and load its models,
    migrations, and related components correctly.
    """

    # The name of the application as referenced in INSTALLED_APPS
    name = "streaks"
