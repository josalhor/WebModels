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
from todo.forms import AssignFormDesigner


@login_required
def designer_assign(request, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    type_task = dict(Task.TYPES_OF_TASK_CHOICES)[task.task_type]
    user_email = request.user
    designer = Designer.objects.filter(user=user_email).first()

    designer_view = designer != None

    if task.assigned_to != None or (designer_view and not designer.chief):
        raise PermissionDenied

    if request.POST:
        form = AssignFormDesigner(request.POST)
        if form.is_valid():
            task.assigned_to = UserInfo.objects.filter(user=form.cleaned_data['designer'].user).first()
            task.save()
            messages.success(request, "La propuesta de ilustracion ha sido correctamente asignada.")
            designer_user_info = UserInfo.objects.filter(user=task.assigned_to).first()
            editor_user_info = task.created_by
            email_body = render_to_string(
                "todo/email/assigned_designer.txt", {"site": Site.objects.get_current().domain, "task": task, "designer": designer_user_info, "type_task": type_task}
            )

            send_mail(
                "Nueva tarea asignada",
                email_body,
                None,
                [designer, task.assigned_to],
                fail_silently=False,
            )
            
        return redirect("todo:task_lists")
    

    context = {
        'designer_view': designer_view,
        'type_task': type_task,
        'creator': task.created_by,
        'description': task.description,
        'task': task,
        'assign_form': AssignFormDesigner(),
        'init_date': task.created_date,
        'end_date': task.due_date
    }
    return render(request, "todo/designer_assign.html", context)