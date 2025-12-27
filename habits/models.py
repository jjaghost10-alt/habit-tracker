from django.db import models
from datetime import date
from django.utils.timezone import now


class Habit(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class HabitCheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("habit", "date")
