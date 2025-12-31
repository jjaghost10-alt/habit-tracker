from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Book, UserBook


def recommend(request):
    """
    Book recommendation page.

    Reads optional filters from query parameters (GET):
    - mood
    - goal
    - minutes (reading time budget)

    Returns:
    - a "Top Pick" recommendation (first result)
    - a list of additional matching books
    - a list of already-saved book IDs (for UI badges like "Saved")
    """
    # For the form dropdowns
    moods = Book.MOODS
    goals = Book.GOALS

    # These will be passed to the template
    recommended = None
    results = []

    # Read filter values from the URL query string (?mood=...&goal=...&minutes=...)
    # We default to "" so missing values do not break the filters.
    mood = request.GET.get("mood", "")
    goal = request.GET.get("goal", "")
    minutes = request.GET.get("minutes", "")

    # Start from the full catalogue, then narrow it down with filters
    queryset = Book.objects.all()

    # Apply filters only if user provided them
    if mood:
        queryset = queryset.filter(mood=mood)
    if goal:
        queryset = queryset.filter(goal=goal)

    # Time preference filter: keep it forgiving with a +/-10 minute window
    # This avoids "no results" too often and feels more user-friendly.
    if minutes:
        try:
            m = int(minutes)
            # keep it forgiving: within +/- 10 minutes
            queryset = queryset.filter(
                minutes_per_day__gte=max(0, m - 10),
                minutes_per_day__lte=m + 10
            )
        except ValueError:
            # If user enters something non-numeric, ignore time filtering
            pass

    # Exclude books the user already marked finished (nice UX)
    finished_ids = []
    if request.user.is_authenticated:
        finished_ids = UserBook.objects.filter(
            user=request.user,
            status="finished"
        ).values_list("book_id", flat=True)
    queryset = queryset.exclude(id__in=finished_ids)

    # Limit results to keep the UI fast and uncluttered
    results = list(queryset[:12])
    if results:
        recommended = results[0]

    # Precompute the user's saved books so the template can show "Saved" state
    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(
            UserBook.objects.filter(user=request.user)
            .values_list("book_id", flat=True)
        )

    # Render the recommendation template
    return render(request, "books/recommend.html", {
        "moods": moods,
        "goals": goals,
        "recommended": recommended,
        "results": results,
        "saved_ids": saved_ids,
        # Helpful for keeping the form state (optional, since we also use request.GET)
        "selected": {"mood": mood, "goal": goal, "minutes": minutes},
    })


def add_to_library(request, book_id):
    """
    Action view: adds a book to the current user's library.

    Uses get_or_create() to prevent duplicate saved books.
    After saving, redirects the user to the library page.
    """
    if not request.user.is_authenticated:
        return redirect("recommend")

    # Fetch the book or return 404 if the ID doesn't exist
    book = get_object_or_404(Book, id=book_id)
    # Create the UserBook relationship if it doesn't exist yet
    UserBook.objects.get_or_create(user=request.user, book=book)
    # Redirect rather than render to avoid double form submissions on refresh
    return redirect("books_library")


def library(request):
    """
    Library page.

    Displays all books saved by the current user, including:
    - reading status
    - progress, rating, notes

    Uses select_related('book') to avoid extra database queries
    when accessing ub.book.title, ub.book.author, etc. in templates.
    """
    user_books = []

    if request.user.is_authenticated:
        user_books = (
            UserBook.objects
            .filter(user=request.user)
            .select_related("book")  # performance optimization (joins Book in one query)
            .order_by("-saved_at")   # most recently saved books first
        )

    return render(request, "books/library.html", {"user_books": user_books})


def book_detail(request, book_id):
    """
    Book detail page.

    Shows one book from the catalogue and the user's personal data for it.
    Ensures a UserBook row exists so the user can immediately start tracking
    progress / notes / rating.
    """
    if not request.user.is_authenticated:
        return redirect("recommend")

    book = get_object_or_404(Book, id=book_id)
    # Ensure the user has a UserBook entry for this book
    userbook, _ = UserBook.objects.get_or_create(user=request.user, book=book)
    return render(request, "books/detail.html", {"book": book, "userbook": userbook})


def update_userbook(request, book_id):
    """
    Action view: updates user-specific book data.

    Accepts POST data from the book detail page:
    - status (want / reading / finished)
    - progress (0–100)
    - rating (1–5 or blank)
    - notes (free text)

    Redirects back to the book detail page after saving.
    """
    if not request.user.is_authenticated:
        return redirect("recommend")

    book = get_object_or_404(Book, id=book_id)
    # Ensure a UserBook object exists before updating
    userbook, _ = UserBook.objects.get_or_create(user=request.user, book=book)

    # Only update if the form was submitted via POST
    if request.method == "POST":
        # Read incoming form fields; fallback to existing values if missing
        status = request.POST.get("status", userbook.status)
        progress = request.POST.get("progress", userbook.progress)
        rating = request.POST.get("rating", "")
        notes = request.POST.get("notes", userbook.notes)

        # Update status directly (it's validated by choices at model/template level)
        userbook.status = status
        try:
            userbook.progress = max(0, min(100, int(progress)))
        except ValueError:
            pass

        # Rating: allow empty rating (= None), otherwise clamp to 1–5
        if rating == "":
            userbook.rating = None
        else:
            try:
                userbook.rating = max(1, min(5, int(rating)))
            except ValueError:
                userbook.rating = None

        # Notes can be any text
        userbook.notes = notes
        # Save updated user-specific book state
        userbook.save()

    # Redirect to the detail page (PRG pattern)
    return redirect("book_detail", book_id=book.id)