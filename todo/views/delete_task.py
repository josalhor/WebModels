from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from todo.models import Task


@login_required
def delete_task(request, task_id: int) -> HttpResponse:
    if request.method == "POST":
        task = get_object_or_404(Task, pk=task_id)

        redir_url = reverse(
            "todo:list_detail",
            kwargs={"list_id": task.book.id, "list_slug": task.book.slug},
        )

        # Permissions
        if task.created_by.user != request.user:
            raise PermissionDenied

        task.delete()

        messages.success(request, "Task '{}' has been deleted".format(task.title))
        return redirect(redir_url)

    else:
        raise PermissionDenied
