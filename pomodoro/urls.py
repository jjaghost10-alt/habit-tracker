from django.urls import path
from . import views

# URL configuration for the Pomodoro feature

urlpatterns = [
    # Starts a new Pomodoro session for the current user
    path("start/", views.start, name="pomodoro_start"),
    # Resets the current Pomodoro session
    path("reset/", views.reset, name="pomodoro_reset"),
]