from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from todo.models import Editor, Task
from todo.utils import toggle_task_completed
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def toggle_done(request, task_id: int) -> HttpResponse:
    if request.method == "POST":
        task = get_object_or_404(Task, pk=task_id)

        redir_url = reverse(
            "todo:list_detail",
            kwargs={"list_id": task.book.id, "list_slug": task.book.slug},
        )

        editor = Editor.objects.filter(user=request.user).first()

        if request.user != task.created_by.user and (not editor.chief):
            raise PermissionDenied

        toggle_task_completed(task.id)
        messages.success(request, "El estado de la tarea '{}' ha sido actualizado".format(task.title))

        return redirect(redir_url)

    else:
        raise PermissionDenied
