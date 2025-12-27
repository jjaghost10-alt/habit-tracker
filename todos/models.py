from django.db import models
from django.utils.timezone import now


class Todo(models.Model):
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title