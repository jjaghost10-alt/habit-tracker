from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    A book that can be recommended.
    """

    # --------------------------------------------------
    # Choice fields used for recommendations
    # --------------------------------------------------

    # The main goal or benefit the book supports
    # (selected by the user during recommendation)
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

    # --------------------------------------------------
    # Core book metadata
    # --------------------------------------------------

    # Book title (required)
    title = models.CharField(max_length=200)
    # Optional author field
    author = models.CharField(max_length=200, blank=True)
    # Short description or summary of the book
    description = models.TextField(blank=True)

    # --------------------------------------------------
    # Recommendation attributes
    # --------------------------------------------------

    # Goal and mood are used to filter and recommend books
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
        """Human-readable representation of the book"""
        return f"{self.title} ({self.author})" if self.author else self.title


class UserBook(models.Model):
    """
    A user's relationship with a book (saved, reading, finished).
    """

    # --------------------------------------------------
    # Reading status choices
    # --------------------------------------------------
    STATUS_CHOICES = [
        ("want", "Want to read"),
        ("reading", "Reading"),
        ("finished", "Finished"),
    ]

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    # The user who saved the book
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The book being tracked by the user
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # --------------------------------------------------
    # Reading state & metadata
    # --------------------------------------------------

    # Current reading status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="want")
    # Timestamp when the book was first saved
    saved_at = models.DateTimeField(auto_now_add=True)
    # Timestamp automatically updated on every change
    updated_at = models.DateTimeField(auto_now=True)
    # Reading progress in percent (0–100)
    progress = models.IntegerField(default=0) # 0 - 100

    # --------------------------------------------------
    # Optional user feedback
    # --------------------------------------------------

    # Optional: user feedback
    rating = models.IntegerField(null=True, blank=True)  # 1–5 later if you want
    notes = models.TextField(blank=True)

    class Meta:
        """
        Ensures that a user can only save a specific book once.
        Prevents duplicate UserBook entries.
        """
        unique_together = ("user", "book")  # prevents duplicates

    def __str__(self):
        """
        Human-readable representation of the user-book relationship.
        """
        return f"{self.user.username} - {self.book.title} ({self.status})"