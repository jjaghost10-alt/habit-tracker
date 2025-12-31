from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
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
    moods = Book.MOODS
    goals = Book.GOALS

    recommended = None
    results = []

    mood = request.GET.get("mood", "")
    goal = request.GET.get("goal", "")
    minutes = request.GET.get("minutes", "")

    queryset = Book.objects.all()

    if mood:
        queryset = queryset.filter(mood=mood)
    if goal:
        queryset = queryset.filter(goal=goal)

    if minutes:
        try:
            m = int(minutes)
            queryset = queryset.filter(
                minutes_per_day__gte=max(0, m - 10),
                minutes_per_day__lte=m + 10
            )
        except ValueError:
            pass

    finished_ids = []
    if request.user.is_authenticated:
        finished_ids = UserBook.objects.filter(
            user=request.user,
            status="finished"
        ).values_list("book_id", flat=True)

    queryset = queryset.exclude(id__in=finished_ids)

    results = list(queryset[:12])
    if results:
        recommended = results[0]

    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(
            UserBook.objects.filter(user=request.user)
            .values_list("book_id", flat=True)
        )

    return render(request, "books/recommend.html", {
        "moods": moods,
        "goals": goals,
        "recommended": recommended,
        "results": results,
        "saved_ids": saved_ids,
        "selected": {"mood": mood, "goal": goal, "minutes": minutes},
    })

from django.contrib.auth import get_user_model
User = get_user_model()

def add_to_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Use a single demo user for no-login mode
    demo_user, _ = User.objects.get_or_create(username="demo")

    UserBook.objects.get_or_create(
        user=demo_user,
        book=book
    )

    return redirect("books")


def library(request):
    User = get_user_model()
    demo_user, _ = User.objects.get_or_create(username="demo")

    user_books = (
        UserBook.objects
        .filter(user=demo_user)
        .select_related("book")
        .order_by("-saved_at")
    )

    return render(request, "books/library.html", {"user_books": user_books})


def book_detail(request, book_id):
    """
    Book detail page.

    Shows one book from the catalogue.
    User-specific data is optional and only loaded for authenticated users.
    """
    book = get_object_or_404(Book, id=book_id)

    userbook = None
    if request.user.is_authenticated:
        userbook, _ = UserBook.objects.get_or_create(
            user=request.user,
            book=book
        )

    return render(
        request,
        "books/detail.html",
        {
            "book": book,
            "userbook": userbook,
        },
    )


from django.contrib.auth import get_user_model
User = get_user_model()

def update_userbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Use the same demo user as everywhere else
    demo_user, _ = User.objects.get_or_create(username="demo")

    userbook, _ = UserBook.objects.get_or_create(
        user=demo_user,
        book=book
    )

    if request.method == "POST":
        status = request.POST.get("status", userbook.status)
        progress = request.POST.get("progress", userbook.progress)
        rating = request.POST.get("rating", "")
        notes = request.POST.get("notes", userbook.notes)

        userbook.status = status

        try:
            userbook.progress = max(0, min(100, int(progress)))
        except ValueError:
            pass

        if rating == "":
            userbook.rating = None
        else:
            try:
                userbook.rating = max(1, min(5, int(rating)))
            except ValueError:
                userbook.rating = None

        userbook.notes = notes
        userbook.save()

    return redirect("book_detail", book_id=book.id)