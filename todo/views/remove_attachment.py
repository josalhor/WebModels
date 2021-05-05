from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from todo.models import Attachment
from todo.utils import remove_attachment_file


@login_required
def remove_attachment(request, attachment_id: int) -> HttpResponse:
    if request.method == "POST":
        attachment = get_object_or_404(Attachment, pk=attachment_id)

        redir_url = reverse("todo:task_detail", kwargs={"task_id": attachment.task.id})

        # Permissions
        if (attachment.added_by != request.user):
            raise PermissionDenied
        
        if remove_attachment_file(attachment.id):
            messages.success(request, f"Archivo {attachment.id} borrado.")
        else:
            messages.error(
                request, f"Lo sentimos, ha habido un problema corrando el archivo {attachment.id}."
            )

        return redirect(redir_url)

    else:
        raise PermissionDenied
