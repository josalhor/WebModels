import datetime
import os
from todo.utils import try_add_epub_version

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
from todo.forms import PublishedBookForm

@login_required
def book_publish(request, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_id)
    user_email = request.user
    editor = Editor.objects.filter(user=user_email).first()

    if editor == None:
        raise PermissionDenied
        
    if (book.editor != editor) and (not editor.chief):
        raise PermissionDenied
    
    if book.completed:
        raise PermissionDenied

    if request.POST:
        form = PublishedBookForm(request.POST)

        if form.is_valid():
            published_book = form.save(commit=False)     
            published_book.book = book

            # Handle uploaded files
            if request.FILES.get("attachment_file_input"):
                file = request.FILES.get("attachment_file_input")

                if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
                    messages.error(request, f"El archivo excede el tamaño máximo permitido.")
                    return redirect(request.path)

                published_book.final_version = file

            else:
                messages.error(request, f"Debes adjuntar la versión maquetada final en pdf, sino no podremos proceder a su publicación.")
                return redirect(request.path)
            
            if request.FILES.get("attachment_image_input"):
                published_book.related_image = request.FILES.get("attachment_image_input")

            published_book.title = request.POST.get("title")
            published_book.book.description = request.POST.get("description")
            published_book.author_text = request.POST.get("author")
            published_book.book.completed = True
            published_book.book.save()
            published_book.save()
            try_add_epub_version(published_book)

            messages.success(request, "¡Enhorabuena! El libro ha sido publicado correctamente.")
            
            ######### Send email to author
            email_body = render_to_string(
                "todo/email/published_book.txt", {"book": book}
            )

            send_mail(
                "Libro publicado",
                email_body,
                None,
                [book.author.user.email],
                fail_silently=False,
            )
        else:
            print(form.errors)
            messages.error(request, "Lo sentimos, el libro no ha podido publicarse.")
            return redirect(request.path)
            
        return redirect("todo:book_detail", book_id=book.id)
    
    context = {
        'book': book,
        'publish_form': PublishedBookForm()
    }
    return render(request, "todo/book_publish.html", context)