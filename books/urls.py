from django.urls import path
from . import views

urlpatterns = [
    path("", views.recommend, name="books"),
    path("library/", views.library, name="books_library"),
    path("<int:book_id>/", views.book_detail, name="book_detail"),

    # actions
    path("add/<int:book_id>/", views.add_to_library, name="add_to_library"),
    path("update/<int:book_id>/", views.update_userbook, name="update_userbook"),
]
