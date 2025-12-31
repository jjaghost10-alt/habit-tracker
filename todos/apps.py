from django.apps import AppConfig

"""
Todos app configuration

This file defines the configuration for the "todos" Django app.
It tells Django how the app is named and allows future customization
(e.g. app labels, verbose names, or startup logic).
"""


class TodosConfig(AppConfig):
    """
    Configuration class for the todos app.

    Django uses this class to register the app internally.
    The 'name' attribute must match the app's Python package name.
    """
    name = "todos"
