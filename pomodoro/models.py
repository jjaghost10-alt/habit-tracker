from django.conf import settings
from django.db import models
from django.utils import timezone

class PomodoroSession(models.Model):
    STATUS_CHOICES = [
        ("running", "Running"),
        ("completed", "Completed"),
        ("stopped", "Stopped"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # optional link to a habit (only if you want it)
    habit = models.ForeignKey("habits.Habit", null=True, blank=True, on_delete=models.SET_NULL)

    duration_seconds = models.PositiveIntegerField(default=25 * 60)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="running")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        mins = self.duration_seconds // 60
        return f"{self.user} - {self.duration_minutes}m ({self.status})"
