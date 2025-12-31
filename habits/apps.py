from django.apps import AppConfig


class HabitsConfig(AppConfig):
    """
    Application configuration for the habits app.

    This class registers the habits application with Django
    and ensures that its models, migrations, and other
    components are loaded correctly at startup.
    """

    # Name of the application as referenced in INSTALLED_APPS
    name = "habits"
