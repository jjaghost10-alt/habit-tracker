from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start, name="pomodoro_start"),
    path("reset/", views.reset, name="pomodoro_reset"),
]

