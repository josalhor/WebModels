from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from todo.defaults import defaults
from todo.forms import AddExternalBookForm, AddBookForm
from todo.models import Book, Editor, Writer, UserInfo
from todo.utils import staff_check
import os

@user_passes_test(staff_check)
def external_add(request) -> HttpResponse:

    if request.POST:
        form = AddExternalBookForm(request.POST)
        form_book = AddBookForm(request.POST)
        
        if form.is_valid() and form_book.is_valid():
            current_site = Site.objects.get_current()
            User = get_user_model()
            email = request.POST['email']
            user = User.objects.filter(email=email).first()
            
            if not user:
                password = User.objects.make_random_password()
                user = User.objects.create_user(email, password)
            user_info = UserInfo.objects.filter(user=user).first()
            if not user_info:
                user_info = form.save(commit=False)
                user_info.user = user
                user_info.save()
            writer, created_writer = Writer.objects.update_or_create(user=user)


            book = form_book.save(commit=False)

            # Handle uploaded files
            if request.FILES.get("attachment_file_input"):
                file = request.FILES.get("attachment_file_input")

                if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
                    messages.error(request, f"El archivo excede el tamaño máximo permitido")
                    return redirect("todo:external_add")

                name, extension = os.path.splitext(file.name)

                if extension not in defaults("TODO_LIMIT_FILE_ATTACHMENTS"):
                    messages.error(request, f"Este sitio no eccepta atchivos de extensión {extension}")
                    return redirect("todo:external_add")

                book.file = file

            else:
                messages.error(request, f"Debes adjuntar un libro.")
                return redirect("todo:external_add")

            book.author = writer
            book.save()


            messages.success(
                request, "Su libro se ha enviado. Nos pondremos en contacto con usted pronto."
            )


            chief_editors = Editor.objects.filter(chief=True).all()
            mails = [e.user.email for e in chief_editors]

            email_subject = render_to_string(
                "todo/email/assigned_subject.txt", {"title": book.name}
            )
            email_body = render_to_string(
                "todo/email/assigned_body.txt", {"site": current_site.domain, "book": book, "from_name": user_info.full_name}
            )
            uid = user_info.reset_unique_id

            if created_writer:
                writer_body = render_to_string(
                    "todo/email/setpassword.txt", {"site": current_site.domain, "user": user_info, "reset_uid": str(uid)}
                )
                writer_subject = "Set Password"
            else:
                writer_body = render_to_string(
                    "todo/email/new_book_no_password.txt", {"site": current_site.domain, "user": user_info, "reset_uid": str(uid)}
                )
                writer_subject = "Libro recibido"

            try:
                ######### Send email to editors
                send_mail(
                    email_subject,
                    email_body,
                    None,
                    mails,
                    fail_silently=False,
                )
                ######### Send email to author

                send_mail(
                    writer_subject,
                    writer_body,
                    None,
                    [email],
                    fail_silently=False,
                )
            except ConnectionRefusedError:
                messages.warning(
                    request, "Error en gestión del libro. Contacte con el administrador."
                )
            
            return redirect(defaults("TODO_PUBLIC_SUBMIT_REDIRECT"))



    else:
        form = AddExternalBookForm(initial={"priority": 999})
        form_book = AddBookForm()

    context = {"form": form, "form_book": form_book}

    return render(request, "todo/add_task_external.html", context)
