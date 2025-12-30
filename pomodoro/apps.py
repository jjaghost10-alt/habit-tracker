from django.apps import AppConfig
"""
    Application configuration for the Pomodoro feature.

    This app provides time-boxed focus sessions (Pomodoro technique)
    that integrate with the habit tracker. The configuration class
    allows Django to properly register the app and provides a place
    for future extensions such as signals or startup logic.
    """

class PomodoroConfig(AppConfig):
    name = 'pomodoro' # The name of the Django app as referenced in INSTALLED_APPS
