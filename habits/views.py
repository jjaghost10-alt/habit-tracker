from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from datetime import date, timedelta
import calendar

from streaks.models import Streak
from .models import Habit, HabitCheckIn

from books.models import UserBook
from pomodoro.models import PomodoroSession


def dashboard(request):
    """
    Main dashboard view.
    Splits habits into 'open' and 'completed today' based on check-ins.
    Also provides today's date and weekday for the UI header.
    """

    # --------------------------------------------------
    # Existing logic
    # --------------------------------------------------

    # Fetch all habits
    habits = Habit.objects.all()

    # Today's date
    today = date.today()

    # --------------------------------------------------
    # Pomodoro Timer
    # --------------------------------------------------
    active_pomodoro = None
    if request.user.is_authenticated:
        active_pomodoro = PomodoroSession.objects.filter(
            user=request.user,
            status="running"
        ).order_by("-started_at").first()

    # IDs of habits completed today
    completed_today = {
        checkin.habit_id
        for checkin in HabitCheckIn.objects.filter(date=today)
    }

    # Calendar logic – currently not used in UI
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

    # --------------------------------------------------
    # User books
    # --------------------------------------------------
    user_books = (
        UserBook.objects
        .select_related("book")
        .order_by("-saved_at")[:3]
    )
    # --------------------------------------------------
    # Weekly habit matrix
    # --------------------------------------------------
    week_days = [
        today - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    weekly_checkins = HabitCheckIn.objects.filter(
        date__in=week_days
    )

    weekly_checkin_map = {
        (checkin.habit_id, checkin.date): True
        for checkin in weekly_checkins
    }

    # --------------------------------------------------
    # Context
    # --------------------------------------------------
    context = {
        "habits": habits,
        "completed_today": completed_today,
        "user_books": user_books,
        "active_pomodoro": active_pomodoro,

        # Header information
        "today": today,
        "weekday": calendar.day_name[today.weekday()],

        # Calendar data
        "days_in_month": range(1, days_in_month + 1),
        "habit_calendar": habit_calendar,

        # Weekly matrix data
        "week_days": week_days,
        "weekly_checkin_map": weekly_checkin_map,
    }

    return render(
        request,
        "habits/dashboard.html",
        context,
    )


def toggle_habit(request, habit_id):
    """
    Toggles today's completion state of a habit.
    """

    habit = get_object_or_404(Habit, id=habit_id)
    today = date.today()

    checkin = HabitCheckIn.objects.filter(
        habit=habit,
        date=today,
    ).first()

    if checkin:
        checkin.delete()
    else:
        HabitCheckIn.objects.create(habit=habit, date=today)
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
    Deletes a habit and all related data.
    """

    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()

    return redirect("dashboard")