import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

from todo.forms import SearchForm
from todo.models import Task, Book, Editor, Writer, Designer


@login_required
def task_lists(request) -> HttpResponse:

    designer = Designer.objects.filter(user=request.user).first()

    if designer:
        lists = Task.objects.filter(assigned_to=None, task_type='I') | Task.objects.filter(assigned_to=None, task_type='M')
        lists = lists.order_by("title")
        list_count = lists.count()
    else:
        author = Writer.objects.filter(user=request.user)
        lists = Book.objects.filter(editor=None, rejected=False, author__in=author).order_by("name")
        list_count = lists.count()

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)  

    context = {
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
    }

    return render(request, "todo/task_lists.html", context)
