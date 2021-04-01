import bleach
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from todo.forms import AddEditTaskForm
from todo.models import Task, Book
from todo.utils import send_notify_mail, staff_check


@login_required
@user_passes_test(staff_check)
def list_detail(request, list_id=None, list_slug=None, view_completed=False) -> HttpResponse:
    """Display and manage tasks in a todo list.
    """

    # Defaults
    book_list = None
    form = None

    # Which tasks to show on this list view?
    if list_slug == "mine":
        tasks = Task.objects.filter(assigned_to=request.user)

    else:
        # Show a specific list, ensuring permissions.
        book_list = get_object_or_404(Book, id=list_id)
        if not request.user.is_superuser:
            raise PermissionDenied
        tasks = Task.objects.filter(book_list=book_list.id)

    # Additional filtering
    if view_completed:
        tasks = tasks.filter(completed=True)
    else:
        tasks = tasks.filter(completed=False)

    # ######################
    #  Add New Task Form
    # ######################

    if request.POST.getlist("add_edit_task"):
        form = AddEditTaskForm(
            request.POST,
            initial={"priority": 999, "book_list": book_list},
        )

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = request.user
            new_task.note = bleach.clean(form.cleaned_data["note"], strip=True)
            form.save()

            # Send email alert only if Notify checkbox is checked AND assignee is not same as the submitter
            if (
                "notify" in request.POST
                and new_task.assigned_to
                and new_task.assigned_to != request.user
            ):
                send_notify_mail(new_task)

            messages.success(request, 'New task "{t}" has been added.'.format(t=new_task.title))
            return redirect(request.path)
        else:
            messages.warning(
                    request,
                    form.errors 
                )
    else:
        # Don't allow adding new tasks on some views
        if list_slug not in ["mine", "recent-add", "recent-complete"]:
            form = AddEditTaskForm(
                initial={"priority": 999, "book_list": book_list},
            )

    context = {
        "list_id": list_id,
        "list_slug": list_slug,
        "book_list": book_list,
        "form": form,
        "tasks": tasks,
        "view_completed": view_completed,
    }

    return render(request, "todo/list_detail.html", context)
