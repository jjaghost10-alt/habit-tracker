from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from calendar import monthrange # for calendar view (added by David)
from streaks.models import Streak # conncection to streaks (added by David)

from .models import Habit, HabitCheckIn


def dashboard(request):
    habits = Habit.objects.all()
    today = date.today()

    # Which habits are completed today (already used by you)
    completed_today = {
        checkin.habit_id
        for checkin in HabitCheckIn.objects.filter(date=today)
    }

    # Calendar logic (NEW)
    year = today.year
    month = today.month
    days_in_month = monthrange(year, month)[1]

    # For each habit: list of completed days in this month
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

    return render(
        request,
        "habits/dashboard.html",
        {
            "habits": habits,
            "completed_today": completed_today,
            "days_in_month": range(1, days_in_month + 1),   # 👈 for calendar
            "habit_calendar": habit_calendar,               # 👈 for checkmarks
        },
    )

def toggle_habit(request, habit_id):
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

        # 🔥 Update streak
        streak, created = Streak.objects.get_or_create(habit=habit)
        streak.update_streak()

    return redirect("dashboard")


from django.views.decorators.http import require_POST

@require_POST
def add_habit(request):
    name = request.POST.get("name")
    if name:
        Habit.objects.create(name=name)
    return redirect("dashboard")

@require_POST
def delete_habit(request, habit_id):
    """
    Deletes a habit and all related data (check-ins, streaks). Added by David.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()
    return redirect("dashboard")
