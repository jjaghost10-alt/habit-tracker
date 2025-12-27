from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from habits.models import Habit
from .models import Streak


def complete_habit(request, habit_id):
    """
    Marks a habit as completed and updates its streak.
    """
    habit = get_object_or_404(Habit, id=habit_id)

    # Get or create streak for this habit
    streak, created = Streak.objects.get_or_create(habit=habit)

    # Update streak logic
    streak.update_streak()

    return HttpResponse(
        f"Habit '{habit.name}' completed. Current streak: {streak.count}"
    )
