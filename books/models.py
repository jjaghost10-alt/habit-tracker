from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    A book that can be recommended.
    """

    # What “kind” of help the book gives (the user will choose one)
    GOALS = [
        ("focus", "Focus"),
        ("sleep", "Sleep"),
        ("fitness", "Fitness"),
        ("mindset", "Mindset"),
        ("productivity", "Productivity"),
        ("stress", "Stress"),
    ]

    # How the user currently feels (the user will choose one)
    MOODS = [
        ("motivated", "Motivated"),
        ("tired", "Tired"),
        ("overwhelmed", "Overwhelmed"),
        ("curious", "Curious"),
        ("calm", "Calm"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # These help recommendations
    goal = models.CharField(max_length=20, choices=GOALS)
    mood = models.CharField(max_length=20, choices=MOODS)

    # Time estimate: “this book fits someone with 10 min/day” etc.
    minutes_per_day = models.IntegerField(default=10)

    # Free tags to match (comma-separated): "habits, discipline, dopamine"
    tags = models.CharField(max_length=300, blank=True)

    def tag_list(self):
        """Turn 'habits, discipline' into ['habits', 'discipline']."""
        return [t.strip().lower() for t in self.tags.split(",") if t.strip()]

    def __str__(self):
        return f"{self.title} ({self.author})" if self.author else self.title


class UserBook(models.Model):
    """
    A user's relationship with a book (saved, reading, finished).
    """

    STATUS_CHOICES = [
        ("want", "Want to read"),
        ("reading", "Reading"),
        ("finished", "Finished"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="want")
    saved_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    progress = models.IntegerField(default=0) # 0 - 100

    # Optional: user feedback
    rating = models.IntegerField(null=True, blank=True)  # 1–5 later if you want
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "book")  # prevents duplicates

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"

