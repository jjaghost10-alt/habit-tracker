from django.urls import path
from . import views

# ---------------------------------------------------------
# URL configuration for the books app
# ---------------------------------------------------------
# This file maps URL paths to view functions that handle
# book recommendations, the user library, and book actions.
# Each URL is given a name so it can be referenced
# easily in templates using the {% url %} tag.
# ---------------------------------------------------------

urlpatterns = [
    # Main entry point for the books feature
    # Displays the recommendation form and suggested books
    path("", views.recommend, name="books"),
    # Displays the user's personal library
    # Shows all books the user has saved, along with progress and notes
    path("library/", views.library, name="books_library"),
    # Detailed view for a single book
    # Allows the user to view metadata and update their reading state
    path("<int:book_id>/", views.book_detail, name="book_detail"),

    # --------------------------------------------------
    # Actions (POST-based operations)
    # --------------------------------------------------

    # Adds a book to the user's library
    # Creates a UserBook entry if it does not already exist
    path("add/<int:book_id>/", views.add_to_library, name="add_to_library"),
    # Updates user-specific book data
    # (status, progress, rating, notes)
    path("update/<int:book_id>/", views.update_userbook, name="update_userbook"),
]