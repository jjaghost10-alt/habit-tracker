from django.db import models

# Create your models here.

from django.db import models
from habits.models import Habit  # Link to the Habit app
from datetime import date


class Streak(models.Model):
    # Each habit has exactly one streak
    habit = models.OneToOneField(
        Habit,
        on_delete=models.CASCADE,
        related_name="streak"
    )

    # Current streak length (number of consecutive days)
    count = models.PositiveIntegerField(default=0)

    # Date when the habit was last completed
    last_completed = models.DateField(null=True, blank=True)

    def update_streak(self):
        """
        Updates the streak based on today's date.
        - If completed yesterday → increment streak
        - If completed today → do nothing
        - Otherwise → reset streak
        """
        today = date.today()

        if self.last_completed == today:
            return  # already counted today

        if self.last_completed == today.replace(day=today.day - 1):
            self.count += 1
        else:
            self.count = 1

        self.last_completed = today
        self.save()

    def __str__(self):
        return f"Streak for {self.habit.name}: {self.count}"