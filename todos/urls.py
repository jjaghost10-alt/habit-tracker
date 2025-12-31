from django.urls import path
from . import views

"""
URL configuration for the todos app

This file defines all URL routes related to the to-do feature.
Each path maps a specific URL pattern to a corresponding
view function that handles the request.
"""

urlpatterns = [
    # Main to-do list page
    # Displays all existing to-do items
    # This route is the entry point for the todos app
    path("", views.todo_list, name="todo_list"),

    # Add a new to-do item
    # Handles POST requests from the add-task form
    path("add/", views.add_todo, name="add_todo"),

    # Toggle completion state of a to-do item
    # Marks a task as done or reverts it back to active
    path("toggle/<int:todo_id>/", views.toggle_todo, name="toggle_todo"),

    # Delete a to-do item
    # Permanently removes the task from the database
    path("delete/<int:todo_id>/", views.delete_todo, name="delete_todo"),
]

