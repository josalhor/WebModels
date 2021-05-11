from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from todo.models import Task, Book
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def del_list(request, list_id: int, list_slug: str) -> HttpResponse:
    book = get_object_or_404(Book, id=list_id)

    # Ensure user has permission to delete list. Get the group this list belongs to,
    # and check whether current user is a member of that group AND a staffer.
    if book.group not in request.user.groups.all():
        raise PermissionDenied    
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        Book.objects.get(id=book.id).delete()
        messages.success(request, "{list_name} is gone.".format(list_name=book.name))
        return redirect("todo:lists")
    else:
        task_count_done = Task.objects.filter(book=book.id, completed=True).count()
        task_count_undone = Task.objects.filter(book=book.id, completed=False).count()
        task_count_total = Task.objects.filter(book=book.id).count()

    context = {
        "book": book,
        "task_count_done": task_count_done,
        "task_count_undone": task_count_undone,
        "task_count_total": task_count_total,
    }

    return render(request, "todo/del_list.html", context)
