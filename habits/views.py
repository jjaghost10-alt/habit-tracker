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

    Renders the central dashboard page of the application.
    Combines multiple features into a single overview:
    - habit tracking (open vs. completed today)
    - active pomodoro session
    - reading progress preview
    - weekly habit consistency matrix
    """

    # --------------------------------------------------
    # Habit data
    # --------------------------------------------------

    # Fetch all habits
    habits = Habit.objects.all()

    # Today's date
    today = date.today()

    # --------------------------------------------------
    # Pomodoro timer
    # --------------------------------------------------

    # Retrieve the currently running pomodoro session (if any)
    active_pomodoro = None
    if request.user.is_authenticated:
        active_pomodoro = (
            PomodoroSession.objects
            .filter(user=request.user, status="running")
            .order_by("-started_at")
            .first()
        )

    # --------------------------------------------------
    # Habits completed today
    # --------------------------------------------------

    # Collect IDs of habits that were completed today
    completed_today = {
        checkin.habit_id
        for checkin in HabitCheckIn.objects.filter(date=today)
    }

    # --------------------------------------------------
    # Monthly calendar data (currently not rendered in UI)
    # --------------------------------------------------

    # Determine current month and number of days
    year = today.year
    month = today.month
    days_in_month = calendar.monthrange(year, month)[1]

    # Build a mapping: habit_id -> set of completed days in the month
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
    # Reading overview (books)
    # --------------------------------------------------

    # Fetch the three most recently saved books
    user_books = (
        UserBook.objects
        .select_related("book")
        .order_by("-saved_at")[:3]
    )

    # --------------------------------------------------
    # Weekly habit matrix
    # --------------------------------------------------

    # Generate a list of the last 7 days (including today)
    week_days = [
        today - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    # Fetch all check-ins for the selected week
    weekly_checkins = HabitCheckIn.objects.filter(
        date__in=week_days
    )

    # Create a lookup dictionary for fast template access
    # Key: (habit_id, date) -> True
    weekly_checkin_map = {
        (checkin.habit_id, checkin.date): True
        for checkin in weekly_checkins
    }

    # --------------------------------------------------
    # Template context
    # --------------------------------------------------

    context = {
        # Habit data
        "habits": habits,
        "completed_today": completed_today,

        # Pomodoro data
        "active_pomodoro": active_pomodoro,

        # Reading preview
        "user_books": user_books,

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
    Action view: toggle today's completion state of a habit.

    If a check-in for today already exists, it is removed.
    Otherwise, a new check-in is created and the habit's
    streak is updated accordingly.
    """

    habit = get_object_or_404(Habit, id=habit_id)
    today = date.today()

    # Check whether the habit was already completed today
    checkin = HabitCheckIn.objects.filter(
        habit=habit,
        date=today,
    ).first()

    if checkin:
        # Undo completion for today
        checkin.delete()
    else:
        # Mark habit as completed today
        HabitCheckIn.objects.create(habit=habit, date=today)

        # Ensure streak exists and update it
        streak, _ = Streak.objects.get_or_create(habit=habit)
        streak.update_streak()

    return redirect("dashboard")


@require_POST
def add_habit(request):
    """
    Action view: create a new habit.

    Reads the habit name from POST data and creates
    a new Habit object. Redirects back to the dashboard.
    """

    name = request.POST.get("name")
    if name:
        Habit.objects.create(name=name)

    return redirect("dashboard")


@require_POST
def delete_habit(request, habit_id):
    """
    Action view: delete a habit.

    Removes the habit and all related data such as
    check-ins and streaks. Redirects back to the dashboard.
    """

    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()

    return redirect("dashboard")
