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
    """Allow authenticated users who don't have access to the rest of the ticket system to file a ticket
    in the list specified in settings (e.g. django-todo can be used a ticket filing system for a school, where
    students can file tickets without access to the rest of the todo system).

    Publicly filed tickets are unassigned unless settings.DEFAULT_ASSIGNEE exists.
    """

    # if not settings.TODO_DEFAULT_LIST_SLUG:
    #     # We do NOT provide a default in defaults
    #     raise RuntimeError(
    #         "This feature requires TODO_DEFAULT_LIST_SLUG: in settings. See documentation."
    #     )

    # if not Book.objects.filter(slug=settings.TODO_DEFAULT_LIST_SLUG).exists():
    #     raise RuntimeError(
    #         "There is no Book with slug specified for TODO_DEFAULT_LIST_SLUG in settings."
    #     )

    if request.POST:
        form = AddExternalTaskForm(request.POST)
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
            writer, _ = Writer.objects.update_or_create(user=user)


            book = form_book.save(commit=False)

            # Handle uploaded files
            if request.POST.get("attachment_file_input"):
                file = request.POST.get("attachment_file_input")

                #if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
                    #messages.error(request, f"File exceeds maximum attachment size.")
                    #return redirect("todo:external_add")

                #name, extension = os.path.splitext(file.name)

                #if extension not in defaults("TODO_LIMIT_FILE_ATTACHMENTS"):
                    #messages.error(request, f"This site does not allow upload of {extension} files.")
                    #return redirect("todo:external_add")

                book.file = file

            else:
                messages.error(request, f"You must attach your book.")
                return redirect("todo:external_add")

            book.author = writer
            book.save()


            messages.success(
                request, "Your book presentation has been submitted. We'll get back to you soon."
            )
            return redirect(defaults("TODO_PUBLIC_SUBMIT_REDIRECT"))

            # Send email to assignee if we have one
            if task.assigned_to:
                email_subject = render_to_string(
                    "todo/email/assigned_subject.txt", {"task": task.title}
                )
                email_body = render_to_string(
                    "todo/email/assigned_body.txt", {"task": task, "site": current_site}
                )
                try:
                    send_mail(
                        email_subject,
                        email_body,
                        task.created_by.email,
                        [task.assigned_to.email],
                        fail_silently=False,
                    )
                except ConnectionRefusedError:
                    messages.warning(
                        request, "Task saved but mail not sent. Contact your administrator."
                    )


    else:
        form = AddExternalTaskForm(initial={"priority": 999})
        form_book = AddBookForm()

    context = {"form": form, "form_book": form_book}

    return render(request, "todo/add_task_external.html", context)
