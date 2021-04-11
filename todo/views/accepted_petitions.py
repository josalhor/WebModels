import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from todo.forms import SearchForm
from todo.models import Task, Book
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def accepted_petitions(request) -> HttpResponse:

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)

    # Superusers see all lists
    lists = Book.objects.exclude(editor=None).order_by("name")

    list_count = lists.exclude(editor=None).count()

    deleted = False

    # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
    if request.user.is_superuser:
        task_count = Task.objects.filter(completed=0).count()
    else:
        task_count = (
            Task.objects.filter(completed=0)
            .count()
        )
    
    if request.method == "POST":
        book = Book.objects.filter(name=request.POST['delete-book']).first()
        deleted = True

        book.editor = None
        book.rejected = True
        book.save()

        messages.success(request, "La petición correspondiente al libro '{}' ha sido eliminada de su lista de peticiones aceptadas.".format(book.name))

    context = {
        "deleted": deleted,
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
    }

    return render(request, "todo/accepted_petitions.html", context)
