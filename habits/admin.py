from django.contrib import admin
from .models import Habit, HabitCheckIn

admin.site.register(Habit)
admin.site.register(HabitCheckIn)