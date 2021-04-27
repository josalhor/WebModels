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
from todo.models import Attachment, Comment, Book, Editor, UserInfo
from todo.forms import AssignForm
from todo.utils import (
    send_email_to_thread_participants,
    staff_check,
    toggle_task_completed,
    user_can_read_task,
)

def send_email_reject_book(book, reasons):
    email_body = render_to_string(
        "todo/email/rejected_book.txt", {"book": book, "reasons": reasons}
    )

    send_mail(
        "Libro rechazado",
        email_body,
        None,
        [book.author.user.email],
        fail_silently=False,
    )

@login_required
def book_assign(request, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_id)
    thematic = dict(Book.THEMATIC)[book.thematic]
    user_email = request.user
    editor = Editor.objects.filter(user=user_email).first()

    editor_view = editor != None

    if book.editor != None or (editor_view and not editor.chief):
        raise PermissionDenied

    if request.POST:
        print(request.POST)
        form = AssignForm(request.POST)
        if form.is_valid():
            book.editor = Editor.objects.filter(id=request.POST['editor']).first()
            book.save()
            messages.success(request, "La propuesta de edición ha sido correctamente asignada.")
            editor_user_info = UserInfo.objects.filter(user=book.editor.user).first()
            author_user_info = UserInfo.objects.filter(user=book.author.user).first()
            email_body = render_to_string(
                "todo/email/assigned_book.txt", {"site": Site.objects.get_current().domain, "book": book, "editor": editor_user_info, "author": author_user_info}
            )

            send_mail(
                "Libro asignado",
                email_body,
                None,
                [book.editor.user.email, book.author.user.email],
                fail_silently=False,
            )
        else:
            messages.success(request, "La propuesta de edición ha sido correctamente rechazada.")
            book.rejected = True
            book.save()

            send_email_reject_book(book, reasons="TODO FILL MOTIVOS")
            
        return redirect("todo:accepted_petitions")
    
    context = {
        'editor_view': editor_view,
        'thematic': thematic,
        'editor_user': editor,
        'note': book.note,
        'book': book,
        'assign_form': AssignForm()
    }
    return render(request, "todo/book_assign.html", context)