from django.conf import settings
from django.db import models
from django.utils import timezone


class PomodoroSession(models.Model):
    """
    Represents a single Pomodoro focus session.

    A PomodoroSession belongs to a user and optionally to a habit.
    It stores timing information and the current status of the session.
    """

    # --------------------------------------------------
    # Possible states of a Pomodoro session
    # --------------------------------------------------
    STATUS_CHOICES = [
        ("running", "Running"),
        ("completed", "Completed"),
        ("stopped", "Stopped"),
    ]

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    # The user who started the Pomodoro session
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Optional link to a habit
    # Allows Pomodoro sessions to be associated with habit tracking,
    # but also supports general focus sessions.
    habit = models.ForeignKey(
        "habits.Habit",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # --------------------------------------------------
    # Timing information
    # --------------------------------------------------

    # Total duration of the session in seconds (default = 25 minutes)
    # Storing seconds simplifies frontend countdown logic.
    duration_seconds = models.PositiveIntegerField(default=25 * 60)

    # Timestamp when the session started
    started_at = models.DateTimeField(default=timezone.now)

    # Timestamp when the session ended (null if still running)
    ended_at = models.DateTimeField(null=True, blank=True)

    # --------------------------------------------------
    # Session state & metadata
    # --------------------------------------------------

    # Current status of the session
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="running"
    )

    # Timestamp when the record was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Human-readable representation of the Pomodoro session.
        Displays the user, session duration in minutes,
        and current status.
        """
        minutes = self.duration_seconds // 60
        return f"{self.user} - {minutes}m ({self.status})"