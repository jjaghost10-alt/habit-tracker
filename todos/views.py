from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Todo


def todo_list(request):
    todos = Todo.objects.order_by("is_done", "-created_at")
    return render(request, "todos/todo_list.html", {"todos": todos})


@require_POST
def add_todo(request):
    title = request.POST.get("title")
    if title:
        Todo.objects.create(title=title)
    return redirect("todo_list")


@require_POST
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect("todo_list")


@require_POST
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect("todo_list")