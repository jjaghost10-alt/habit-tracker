from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("habits.urls")),
    path("streaks/", include("streaks.urls")),# neu hinzugefügt von David
]