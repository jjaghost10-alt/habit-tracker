from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("habits.urls")),
    path("streaks/", include("streaks.urls")),# neu hinzugefügt von David
    path("todos/", include("todos.urls")),   # neu hinzugefügt von David
    path("books/", include("books.urls"))    # neu hinzugefügt von Iri
]