from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from todo.models import Task
from todo.utils import toggle_task_completed
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def toggle_done(request, task_id: int) -> HttpResponse:
    """Toggle the completed status of a task from done to undone, or vice versa.
    Redirect to the list from which the task came.
    """

    if request.method == "POST":
        task = get_object_or_404(Task, pk=task_id)

        redir_url = reverse(
            "todo:list_detail",
            kwargs={"list_id": task.book_list.id, "list_slug": task.book_list.slug},
        )

        if (not request.user.is_superuser) and (request.user != task.created_by.user):
            raise PermissionDenied

        toggle_task_completed(task.id)
        messages.success(request, "Task status changed for '{}'".format(task.title))

        return redirect(redir_url)

    else:
        raise PermissionDenied