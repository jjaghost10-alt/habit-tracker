from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Todo


def todo_list(request):
    """
    To-do list page.

    Retrieves all to-do items from the database and displays them
    in a single list. Incomplete tasks are shown first, followed
    by completed tasks. Newer tasks appear before older ones.
    """
    todos = Todo.objects.order_by("is_done", "-created_at")
    return render(request, "todos/todo_list.html", {"todos": todos})


@require_POST
def add_todo(request):
    """
    Action view: add a new to-do item.

    Reads the task title from POST data and creates a new Todo
    object if a title is provided. After creation, redirects
    back to the main to-do list page.
    """
    title = request.POST.get("title")
    if title:
        Todo.objects.create(title=title)
    return redirect("todo_list")


@require_POST
def toggle_todo(request, todo_id):
    """
    Action view: toggle the completion state of a to-do item.

    Fetches the specified to-do item and flips its `is_done` flag.
    This allows the same action to mark a task as completed or
    revert it back to an active state.
    """
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect("todo_list")


@require_POST
def delete_todo(request, todo_id):
    """
    Action view: delete a to-do item.

    Permanently removes the specified task from the database.
    After deletion, redirects back to the to-do list page.
    """
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect("todo_list")
