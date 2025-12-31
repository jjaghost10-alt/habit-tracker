from django.db import models
from habits.models import Habit
from datetime import date


class Streak(models.Model):
    """
    Represents the streak state of a habit.

    A streak tracks how many consecutive days a habit has been completed,
    when it was last completed, and what the longest streak ever achieved was.
    Each habit is associated with exactly one streak.
    """

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    # One-to-one relationship: each habit has exactly one streak
    habit = models.OneToOneField(
        Habit,
        on_delete=models.CASCADE,
        related_name="streak"
    )

    # --------------------------------------------------
    # Streak state
    # --------------------------------------------------

    # Current number of consecutive completed days
    count = models.PositiveIntegerField(default=0)

    # Maximum streak length ever achieved for this habit
    longest_streak = models.PositiveIntegerField(default=0)

    # Date on which the habit was last marked as completed
    last_completed = models.DateField(null=True, blank=True)

    def update_streak(self):
        """
        Update the streak based on today's date.

        Logic:
        - If the habit was already completed today, do nothing.
        - If the habit was completed yesterday, increment the streak.
        - Otherwise, reset the streak to 1.
        - Update the longest streak if the current streak exceeds it.
        """
        today = date.today()

        # Prevent double-counting on the same day
        if self.last_completed == today:
            return

        # Continue streak if habit was completed yesterday
        if self.last_completed == today.replace(day=today.day - 1):
            self.count += 1
        else:
            # Break in streak: start over
            self.count = 1

        # Keep track of the longest streak achieved
        if self.count > self.longest_streak:
            self.longest_streak = self.count

        # Update last completion date and persist changes
        self.last_completed = today
        self.save()

    def __str__(self):
        """
        Human-readable representation of the streak.
        """
        return f"Streak for {self.habit.name}: {self.count}"
