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
from todo.forms import AddExternalTaskForm, AddBookForm
from todo.models import Book, Editor, Writer, UserInfo
from todo.utils import staff_check


@user_passes_test(staff_check)
def external_add(request) -> HttpResponse:

    if request.POST:
        form = AddExternalTaskForm(request.POST)
        form_book = AddBookForm(request.POST)

        print(form_book.is_valid())
        print(form_book.errors)
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
            writer, _ = Writer.objects.update_or_create(user=user)

            book = form_book.save(commit=False)
            book.author = writer
            book.save()


            
            messages.success(
                request, "El teu llibre s'ha enviat. Ens possarem amb contacte amb tu aviat."
            )


            # Send email to assignee if we have one
            chief_editors = Editor.objects.filter(chief=True).all()
            mails = [e.user.email for e in chief_editors]

            email_subject = render_to_string(
                "todo/email/assigned_subject.txt", {"title": book.name}
            )
            email_body = render_to_string(
                "todo/email/assigned_body.txt", {"site": current_site, "book": book, "from_name": user_info.full_name}
            )
            try:
                sent = send_mail(
                    email_subject,
                    email_body,
                    None,
                    mails,
                    fail_silently=False,
                )
                assert sent == 1
                print(sent)
            except ConnectionRefusedError:
                messages.warning(
                    request, "Book saved but mail not sent. Contact your administrator."
                )
            return redirect(defaults("TODO_PUBLIC_SUBMIT_REDIRECT"))



    else:
        form = AddExternalTaskForm(initial={"priority": 999})
        form_book = AddBookForm()

    context = {"form": form, "form_book": form_book}

    return render(request, "todo/add_task_external.html", context)
