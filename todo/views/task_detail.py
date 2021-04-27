import datetime
import os

import bleach
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail

from todo.defaults import defaults
from todo.features import HAS_TASK_MERGE
from todo.forms import AddEditTaskForm
from todo.models import Attachment, Comment, Task, Editor
from todo.utils import (
    send_email_to_thread_participants,
    staff_check,
    toggle_task_completed,
    user_can_read_task,
)

if HAS_TASK_MERGE:
    from dal import autocomplete


def handle_add_comment(request, task):
    if not request.POST.get("add_comment"):
        return

    Comment.objects.create(
        author=request.user.user_info, task=task, body=bleach.clean(request.POST["comment-body"], strip=True)
    )

    send_email_to_thread_participants(
        task,
        request.POST["comment-body"],
        request.user,
        subject='New comment posted on task "{}"'.format(task.title),
    )

    messages.success(request, "Comentario publicado. Los implicados serán avisados por email.")


@login_required
@user_passes_test(staff_check)
def task_detail(request, task_id: int) -> HttpResponse:
    """View task details. Allow task details to be edited. Process new comments on task.
    """
    editor = Editor.objects.filter(user=request.user).first()
    editor_view = False
    if editor != None: editor_view = True
    
    task = get_object_or_404(Task, pk=task_id)
    comment_list = Comment.objects.filter(task=task_id).order_by("-date")

    # Ensure user has permission to view task. Superusers can view all tasks.
    # Get the group this task belongs to, and check whether current user is a member of that group.
    if not user_can_read_task(task, request.user):
        raise PermissionDenied

    # Handle task merging
    if not HAS_TASK_MERGE:
        merge_form = None
    else:

        class MergeForm(forms.Form):
            merge_target = forms.ModelChoiceField(
                queryset=Task.objects.all(),
                widget=autocomplete.ModelSelect2(
                    url=reverse("todo:task_autocomplete", kwargs={"task_id": task_id})
                ),
            )

        # Handle task merging
        if not request.POST.get("merge_task_into"):
            merge_form = MergeForm()
        else:
            merge_form = MergeForm(request.POST)
            if merge_form.is_valid():
                merge_target = merge_form.cleaned_data["merge_target"]
            if not user_can_read_task(merge_target, request.user):
                raise PermissionDenied

            task.merge_into(merge_target)
            return redirect(reverse("todo:task_detail", kwargs={"task_id": merge_target.pk}))

    # Save submitted comments
    handle_add_comment(request, task)

    # Save task edits
    if not request.POST.get("add_edit_task"):
        form = AddEditTaskForm(instance=task, initial={"book_list": task.book_list})
    else:
        form = AddEditTaskForm(
            request.POST, instance=task, initial={"book_list": task.book_list}
        )

        if form.is_valid():
            item = form.save(commit=False)
            item.note = bleach.clean(form.cleaned_data["note"], strip=True)
            item.title = bleach.clean(form.cleaned_data["title"], strip=True)
            item.save()
            messages.success(request, "The task has been edited.")
            return redirect(
                "todo:list_detail", list_id=task.book_list.id, list_slug=task.book_list.slug
            )

    # Mark complete
    if request.POST.get("toggle_done"):
        results_changed = toggle_task_completed(task.id)
        if results_changed:
            messages.success(request, f"Estado de la tarea {task.id} cambiado")

        return redirect("todo:task_detail", task_id=task.id)

    if task.due_date:
        thedate = task.due_date
    else:
        thedate = datetime.datetime.now()

    # Handle uploaded files
    if request.FILES.get("attachment_file_input"):
        file = request.FILES.get("attachment_file_input")

        if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
            messages.error(request, f"El tamaño del archivo supera el máximo admitido.")
            return redirect("todo:task_detail", task_id=task.id)

        name, extension = os.path.splitext(file.name)

        if extension not in defaults("TODO_LIMIT_FILE_ATTACHMENTS"):
            messages.error(request, f"No se admiten archivos {extension}.")
            return redirect("todo:task_detail", task_id=task.id)

        Attachment.objects.create(
            task=task, added_by=request.user, timestamp=datetime.datetime.now(), file=file
        )
        messages.success(request, f"Archivo correctamente adjuntado")

        # Send mail new attachment
        email_body = render_to_string(
            "todo/email/new_attachment.txt",
            {"task": task, "site": Site.objects.get_current(), "user_info": request.user.user_info},
        )

        send_email_to_thread_participants(task, email_body, request.user, subject="Nuevo archivo adjunto")

        return redirect("todo:task_detail", task_id=task.id)


    context = {
        "editor_view": editor_view,
        "task": task,
        "comment_list": comment_list,
        "form": form,
        "merge_form": merge_form,
        "thedate": thedate,
        "comment_classes": defaults("TODO_COMMENT_CLASSES"),
        "attachments_enabled": defaults("TODO_ALLOW_FILE_ATTACHMENTS"),
    }

    return render(request, "todo/task_detail.html", context)
