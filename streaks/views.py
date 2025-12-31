from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from habits.models import Habit
from .models import Streak


def complete_habit(request, habit_id):
    """
    Action view: mark a habit as completed for today.

    This view retrieves the specified habit, ensures that a corresponding
    streak object exists, and updates the streak based on today's date.
    It returns a simple HTTP response confirming the completion and
    showing the current streak length.
    """
    # Fetch the habit or return 404 if the ID does not exist
    habit = get_object_or_404(Habit, id=habit_id)

    # Ensure a streak object exists for this habit
    # If none exists yet, it will be created automatically
    streak, created = Streak.objects.get_or_create(habit=habit)

    # Update the streak according to completion logic
    streak.update_streak()

    # Return a simple confirmation response
    return HttpResponse(
        f"Habit '{habit.name}' completed. Current streak: {streak.count}"
    )
