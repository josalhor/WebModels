import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

from todo.forms import SearchForm
from todo.models import Task, Book, Editor
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def list_lists(request) -> HttpResponse:

    editor = Editor.objects.filter(user=request.user).first()
    if not editor or not editor.chief:
        raise PermissionDenied

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)

    # Superusers see all lists
    lists = Book.objects.filter(editor=None, rejected=False).order_by("name")

    list_count = lists.filter(editor=None).count()

    # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
    if request.user.is_superuser:
        task_count = Task.objects.filter(completed=0).count()
    else:
        task_count = (
            Task.objects.filter(completed=0)
            .count()
        )

    context = {
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
    }

    return render(request, "todo/list_lists.html", context)
