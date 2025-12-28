from django.contrib import admin
from .models import Book, UserBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "goal", "mood", "minutes_per_day")
    search_fields = ("title", "author", "tags")
    list_filter = ("goal", "mood")


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "saved_at")
    list_filter = ("status",)
    search_fields = ("user__username", "book__title")
