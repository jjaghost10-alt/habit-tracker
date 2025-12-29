from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Book, UserBook

@login_required
def recommend(request):
    # For the form dropdowns
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
            # keep it forgiving: within +/- 10 minutes
            queryset = queryset.filter(
                minutes_per_day__gte=max(0, m - 10),
                minutes_per_day__lte=m + 10
)
        except ValueError:
            pass

    # Exclude books the user already marked finished (nice UX)
    finished_ids = UserBook.objects.filter(user=request.user, status="finished").values_list("book_id", flat=True)
    queryset = queryset.exclude(id__in=finished_ids)

    results = list(queryset[:12])
    if results:
        recommended = results[0]

    # user's saved books (so we can show "Saved" on cards)
    saved_ids = set(UserBook.objects.filter(user=request.user).values_list("book_id", flat=True))

    return render(request, "books/recommend.html", {
        "moods": moods,
        "goals": goals,
        "recommended": recommended,
        "results": results,
        "saved_ids": saved_ids,
        "selected": {"mood": mood, "goal": goal, "minutes": minutes},
    })


@login_required
def add_to_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    UserBook.objects.get_or_create(user=request.user, book=book)
    return redirect("books_library")


@login_required
def library(request):
    user_books = (
        UserBook.objects
        .filter(user=request.user)
        .select_related("book")
        .order_by("-saved_at")
    )
    return render(request, "books/library.html", {"user_books": user_books})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    userbook, _ = UserBook.objects.get_or_create(user=request.user, book=book)
    return render(request, "books/detail.html", {"book": book, "userbook": userbook})


@login_required
def update_userbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    userbook, _ = UserBook.objects.get_or_create(user=request.user, book=book)

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