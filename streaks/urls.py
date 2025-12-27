from django.urls import path
from . import views

urlpatterns = [
    path("complete/<int:habit_id>/", views.complete_habit, name="complete-habit"),
]