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
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from todo.defaults import defaults
from todo.models import Attachment, Comment, UserInfo, Task, Designer
from todo.forms import AssignForm
from todo.utils import (
    send_email_to_thread_participants,
    staff_check,
    toggle_task_completed,
    user_can_read_task,
)

"""def send_email_reject_book(book, reasons):
    email_body = render_to_string(
        "todo/email/rejected_book.txt", {"book": book, "reasons": reasons}
    )

    send_mail(
        "Libro rechazado",
        email_body,
        None,
        [book.author.user.email],
        fail_silently=False,
    )"""

@login_required
def designer_assign(request, task_id: int) -> HttpResponse:
    task = get_object_or_404(Book, pk=task_id)
    type_task = dict(Task.TYPES_OF_TASK_CHOICES)[task.task_type]
    user_email = request.user
    designer = Designer.objects.filter(user=user_email).first()

    designer_view = designer != None

    if task.assigned_to != None or (designer_view and not designer.chief):
        raise PermissionDenied

    if request.POST:
        print(request.POST)
        form = AssignFormDesigner(request.POST)
        if form.is_valid():
            task.assigned_to = Designer.objects.filter(id=request.POST['designer']).first()
            task.save()
            messages.success(request, "La propuesta de ilustracion ha sido correctamente asignada.")
            editor_user_info = UserInfo.objects.filter(user=task.created_by.user).first()
            designer_user_info = UserInfo.objects.filter(user=task.assigned_to.user).first()
            """email_body = render_to_string(
                "todo/email/assigned_designer.txt", {"site": Site.objects.get_current().domain, "book": book, "editor": editor_user_info, "author": author_user_info}
            )

            send_mail(
                "Libro asignado",
                email_body,
                None,
                [book.editor.user.email, book.author.user.email],
                fail_silently=False,
            )"""
        else:
            messages.success(request, "La propuesta de ilustracion ha sido correctamente rechazada.")

            """send_email_reject_book(book, reasons=request.POST['reasons'])"""
            
        return redirect("todo:accepted_petitions")
    
    context = {
        'designer_view': designer_view,
        'type_task': type_task,
        'creator': task.created_by,
        'note': task.note,
        'task': task,
        'assign_form': AssignFormDesigner(),
        'init_date': task.created_date,
        'end_date': task.due_date
    }
    return render(request, "todo/designer_assign.html", context)