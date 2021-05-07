import bleach
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from todo.forms import AddEditTaskForm
from todo.models import Task, Book, Writer, Editor, UserInfo
from todo.utils import send_notify_mail, staff_check, user_can_read_book


@login_required
@user_passes_test(staff_check)
def list_detail(request, list_id=None, list_slug=None, view_completed=False) -> HttpResponse:

    # Defaults
    completed = False
    book_list = None
    form = None
    editor_view = False

    editor = Editor.objects.filter(user=request.user).first()
    if editor != None: editor_view = True
    # Which tasks to show on this list view?
    if list_slug == "mine":
        tasks = Task.objects.filter(assigned_to=request.user.user_info)
    else:
        # Show a specific list, ensuring permissions.
        book_list = get_object_or_404(Book, id=list_id)
        if not user_can_read_book(book_list, request.user):
            raise PermissionDenied
        tasks = Task.objects.filter(book_list=book_list.id)
    
    # Check if it can be published
    for task in tasks:
        if task.task_type == task.REVISION and task.completed:
            completed = True

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
            new_task.created_by = editor
            if new_task.task_type == Task.WRITING or new_task.task_type == Task.REVISION:
                new_task.assigned_to = UserInfo.objects.filter(user=book_list.author.user).first()
            new_task.note = bleach.clean(form.cleaned_data["note"], strip=True)
            new_task.save()

            send_notify_mail(new_task)

            messages.success(request, 'La nueva tarea "{t}" ha sido añadida.'.format(t=new_task.title))
            return redirect(request.path)

    else:
        # Don't allow adding new tasks on some views
        if list_slug not in ["mine", "recent-add", "recent-complete"]:
            form = AddEditTaskForm(
                initial={"priority": 999, "book_list": book_list},
            )
    
    context = {
        "completed": completed,
        "editor_view": editor_view,
        "list_id": list_id,
        "list_slug": list_slug,
        "book_list": book_list,
        "form": form,
        "tasks": tasks,
        "view_completed": view_completed,
    }

    return render(request, "todo/list_detail.html", context)
