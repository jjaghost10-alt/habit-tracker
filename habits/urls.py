# selber erstellt
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("toggle/<int:habit_id>/", views.toggle_habit, name="toggle_habit"),
    path("add/", views.add_habit, name="add_habit"),
]
