from django.urls import path
from . import views

urlpatterns = [
    path("", views.books, name="books"),
    path("library/", views.library, name="library"),
    path("library/update/<int:book_id>/", views.update_book_status, name="update_book_status"),
]
