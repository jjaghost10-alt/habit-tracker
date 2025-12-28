from django.shortcuts import render

def books(request):
    return render(request, "books/books.html")

from django.http import HttpResponse

def books(request):
    return HttpResponse("Books page works ✅")

def library(request):
    return HttpResponse("Library page works ✅")

def update_book_status(request, book_id):
    return HttpResponse(f"Update status for book {book_id} ✅")
