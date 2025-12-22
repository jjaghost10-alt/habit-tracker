from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .models import Habit, HabitCheckIn


def dashboard(request):
    habits = Habit.objects.all()

    today = date.today()
    completed_today = {
        checkin.habit_id
        for checkin in HabitCheckIn.objects.filter(date=today)
    }

    return render(
        request,
        "habits/dashboard.html",
        {
            "habits": habits,
            "completed_today": completed_today,
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
        checkin.delete()
    else:
        HabitCheckIn.objects.create(habit=habit, date=today)

    return redirect("dashboard")


from django.views.decorators.http import require_POST

@require_POST
def add_habit(request):
    name = request.POST.get("name")
    if name:
        Habit.objects.create(name=name)
    return redirect("dashboard")
