from django.contrib import admin
from .models import Habit, HabitCheckIn


# Register the Habit model with the Django admin interface.
# This allows administrators to create, edit, and delete habits
# directly via the built-in admin dashboard.
admin.site.register(Habit)


# Register the HabitCheckIn model with the Django admin interface.
# This enables inspection and management of daily habit completion
# records, which are used for streak calculations and statistics.
admin.site.register(HabitCheckIn)
