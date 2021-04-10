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
from todo.models import Attachment, Comment, Book, Editor
from todo.forms import AssignForm
from todo.utils import (
    send_email_to_thread_participants,
    staff_check,
    toggle_task_completed,
    user_can_read_task,
)

@login_required
def book_assign(request, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_id)
    
    context = {
        'assign_form': AssignForm()
    }
    return render(request, "todo/book_assign.html", context)