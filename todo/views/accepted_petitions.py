import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from todo.forms import SearchForm
from todo.models import Task, Book, Editor, Writer
from todo.utils import staff_check


@login_required
@user_passes_test(staff_check)
def accepted_petitions(request) -> HttpResponse:
    deleted, editor_view = False, False

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)

    editor = Editor.objects.filter(user=request.user).first()

    if editor:
        lists = Book.objects.exclude(editor=None, rejected=True).order_by("name")
        editor_view = True
    else:
        author = Writer.objects.filter(user=request.user)
        lists = Book.objects.filter(rejected=False, author__in=author).order_by("name")
        lists = lists.exclude(editor=None)
    
    list_count = lists.count()

    task_count = 0
    for book in lists:
        tasks = Task.objects.filter(book_list=book).count()
        task_count += tasks
        
    
    if request.method == "POST":
        book = Book.objects.filter(name=request.POST['delete-book']).first()
        deleted = True

        book.editor = None
        book.rejected = True
        book.save()

        messages.success(request, "La petición correspondiente al libro '{}' ha sido eliminada de su lista de peticiones aceptadas.".format(book.name))

    context = {
        "editor_view": editor_view,
        "deleted": deleted,
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
    }

    return render(request, "todo/accepted_petitions.html", context)
