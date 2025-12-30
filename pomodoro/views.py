from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import PomodoroSession


@require_POST
def start(request):
    # --------------------------------------------------
    # If user is NOT logged in → guest pomodoro (no DB)
    # --------------------------------------------------
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "running",
            "seconds": 25 * 60,
        })

    # --------------------------------------------------
    # Logged-in user → DB-backed pomodoro
    # --------------------------------------------------
    PomodoroSession.objects.filter(
        user=request.user,
        status="running"
    ).update(status="finished")

    session = PomodoroSession.objects.create(
        user=request.user,
        status="running",
        duration_seconds=25 * 60,
        started_at=timezone.now(),
    )

    return JsonResponse({
        "status": "running",
        "seconds": session.duration_seconds,
    })


@require_POST
def reset(request):
    # --------------------------------------------------
    # Guest → just reset frontend state
    # --------------------------------------------------
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "ready",
            "seconds": 25 * 60,
        })

    # --------------------------------------------------
    # Logged-in user → DB reset
    # --------------------------------------------------
    PomodoroSession.objects.filter(
        user=request.user,
        status__in=["running", "paused"]
    ).update(status="finished")

    return JsonResponse({
        "status": "ready",
        "seconds": 25 * 60,
    })