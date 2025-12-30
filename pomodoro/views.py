from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import PomodoroSession

@login_required
@require_POST
def start(request):
    """
    Starts a new Pomodoro session for the current user.
    """
    # Ensure only one active session exists by finishing any running ones
    PomodoroSession.objects.filter(user=request.user, status="running").update(status="finished")

    # Create a new running Pomodoro session (25 minutes)
    session = PomodoroSession.objects.create(
        user=request.user,
        status="running",
        duration_seconds=25 * 60,
        started_at=timezone.now(),
    )
    # Return JSON data for frontend timer initialization
    return JsonResponse({
        "status": "running",
        "seconds": session.duration_seconds,
    })

@login_required
@require_POST
def reset(request):
    """
    Resets the current Pomodoro session.
    """
    # Stop any active or paused sessions for the user
    PomodoroSession.objects.filter(user=request.user, status__in=["running", "paused"]).update(status="finished")
    # Return default timer state to the frontend
    return JsonResponse({
        "status": "ready",
        "seconds": 25 * 60,
    })