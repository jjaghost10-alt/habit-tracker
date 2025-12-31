from django.db import models
from django.utils.timezone import now

"""
Todo model

This model represents a single to-do item created by a user.
Each to-do consists of a short title, a completion state,
and a timestamp indicating when it was created.
"""


class Todo(models.Model):
    """
    A single to-do item.

    Stores the task title, whether the task has been completed,
    and the creation time. The model is intentionally simple
    and serves as the core data structure for the to-do feature.
    """

    # Short text describing the task
    title = models.CharField(max_length=200)

    # Indicates whether the task has been completed
    is_done = models.BooleanField(default=False)

    # Timestamp when the to-do item was created
    # Uses the current timezone-aware time as default
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        """
        Human-readable representation of the to-do item.

        Used in the Django admin interface and shell
        to display the task by its title.
        """
        return self.title
