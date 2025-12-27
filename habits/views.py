from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from datetime import date
import calendar

from streaks.models import Streak
from .models import Habit, HabitCheckIn


def dashboard(request):
    """
    Main dashboard view.
    Splits habits into 'open' and 'completed today' based on check-ins.
    Also provides today's date and weekday for the UI header.
    """

    # Fetch all habits
    habits = Habit.objects.all()

    # Today's date
    today = date.today()

    # IDs of habits completed today
    completed_today = {
        checkin.habit_id
        for checkin in HabitCheckIn.objects.filter(date=today)
    }

    # (Optional) Calendar logic – currently not used in UI,
    # but kept for future extensions
    year = today.year
    month = today.month
    days_in_month = calendar.monthrange(year, month)[1]

    habit_calendar = {}
    for habit in habits:
        checkins = HabitCheckIn.objects.filter(
            habit=habit,
            date__year=year,
            date__month=month,
        )
        habit_calendar[habit.id] = {
            checkin.date.day for checkin in checkins
        }

    # Context passed to the template
    context = {
        "habits": habits,
        "completed_today": completed_today,

        # Header information
        "today": today,
        "weekday": calendar.day_name[today.weekday()],

        # Calendar data (currently unused in dashboard.html)
        "days_in_month": range(1, days_in_month + 1),
        "habit_calendar": habit_calendar,
    }

    return render(
        request,
        "habits/dashboard.html",
        context,
    )


def toggle_habit(request, habit_id):
    """
    Toggles today's completion state of a habit.
    - If already completed today → undo
    - If not completed → create check-in and update streak
    """

    habit = get_object_or_404(Habit, id=habit_id)
    today = date.today()

    checkin = HabitCheckIn.objects.filter(
        habit=habit,
        date=today,
    ).first()

    if checkin:
        # Habit was already completed today → undo check-in
        checkin.delete()
    else:
        # Create today's check-in
        HabitCheckIn.objects.create(habit=habit, date=today)

        # Update streak (create if it does not exist yet)
        streak, _ = Streak.objects.get_or_create(habit=habit)
        streak.update_streak()

    return redirect("dashboard")


@require_POST
def add_habit(request):
    """
    Creates a new habit from the dashboard modal.
    """

    name = request.POST.get("name")
    if name:
        Habit.objects.create(name=name)

    return redirect("dashboard")


@require_POST
def delete_habit(request, habit_id):
    """
    Deletes a habit and all related data
    (check-ins and streak via cascade).
    """

    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()

    return redirect("dashboard")