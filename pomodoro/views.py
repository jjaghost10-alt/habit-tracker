from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import PomodoroSession

@login_required
@require_POST
def start(request):
    # stop any running sessions
    PomodoroSession.objects.filter(user=request.user, status="running").update(status="finished")

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

@login_required
@require_POST
def reset(request):
    PomodoroSession.objects.filter(user=request.user, status__in=["running", "paused"]).update(status="finished")
    return JsonResponse({
        "status": "ready",
        "seconds": 25 * 60,
    })


