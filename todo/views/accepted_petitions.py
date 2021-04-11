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
    deleted, editor = False, False

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)

    editor = Editor.objects.filter(user=request.user).first()
    writer = Writer.objects.filter(user=request.user).first()

    if editor:
        if request.user.is_superuser:
            # Superusers see all lists
            lists = Book.objects.filter(editor=None, rejected=False).order_by("name")
        else:
            lists = lists.filter(editor=editor) 
        editor = True
    else:
        author = Writer.objects.filter(user=request.user)
        lists = Book.objects.filter(rejected=False, author__in=author).order_by("name")
        print(lists)
        lists = lists.exclude(editor=None)
        print(lists)
    
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
        "editor": editor,
        "deleted": deleted,
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
    }

    return render(request, "todo/accepted_petitions.html", context)
