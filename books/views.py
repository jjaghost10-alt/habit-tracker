from django.shortcuts import render

def books(request):
    return render(request, "books/books.html")

from django.shortcuts import render
from .models import Book

def books(request):
    all_books = Book.objects.all()
    return render(request, "books/books.html", {"books": all_books})

def library(request):
    return HttpResponse("Library page works ✅")

def update_book_status(request, book_id):
    return HttpResponse(f"Update status for book {book_id} ✅")
