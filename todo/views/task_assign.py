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

from todo.defaults import defaults
from todo.models import Attachment, Comment, Task, Editor
from todo.forms import AssignForm
from todo.utils import (
    send_email_to_thread_participants,
    staff_check,
    toggle_task_completed,
    user_can_read_task,
)

@login_required
def task_assign(request, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    
    context = {
        'assign_form': AssignForm()
    }
    return render(request, "todo/task_assign.html", context)