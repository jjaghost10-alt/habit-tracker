from django.contrib import admin
from .models import Book, UserBook

# ---------------------------------------------------------
# Admin configuration for the Book model
# ---------------------------------------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields displayed in the admin list view (table)
    list_display = ("title", "author", "goal", "mood", "minutes_per_day")
    # Enables search functionality by these fields
    # Useful for quickly finding books by title, author, or tags
    search_fields = ("title", "author", "tags")
    # Adds sidebar filters to narrow down the book list
    # Helps with managing and categorizing the book catalogue
    list_filter = ("goal", "mood")

# ---------------------------------------------------------
# Admin configuration for the UserBook model
# ---------------------------------------------------------
@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    # Fields shown in the admin list view
    # Allows administrators to see which user saved which book
    list_display = ("user", "book", "status", "saved_at")
    # Enables filtering by reading status (want / reading / finished)
    list_filter = ("status",)
    # Enables searching by username and book title
    # Double underscore (__) allows searching across relationships
    search_fields = ("user__username", "book__title")