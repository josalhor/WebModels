import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from .book_assign import send_email_reject_book

from todo.forms import SearchForm
from todo.models import Task, Book, Editor, Writer


@login_required
def accepted_petitions(request) -> HttpResponse:
    deleted, editor_view = False, False

    thedate = datetime.datetime.now()
    searchform = SearchForm(auto_id=False)

    editor = Editor.objects.filter(user=request.user).first()
    is_chief = False
    all_lists = None

    if editor:
        lists = Book.objects.filter(completed=False)
        all_lists = Book.objects.filter(completed=False)
        if editor.chief:
            is_chief = True
            lists = lists.filter(editor=editor)
            all_lists = all_lists.exclude(editor=None)
        else:
            lists = lists.filter(editor=editor)
        lists = lists.exclude(rejected=True).order_by("name")
        editor_view = True
    else:
        author = Writer.objects.filter(user=request.user)
        lists = Book.objects.filter(completed=False, rejected=False, author__in=author).exclude(editor=None).order_by("name")
    
    list_count = lists.count()

    task_count = 0
    for book in lists:
        tasks = Task.objects.filter(book=book, completed=False).count()
        task_count += tasks
    

    if request.method == "POST":
        book = Book.objects.filter(name=request.POST['delete-book']).first()
        deleted = True

        book.editor = None
        book.rejected = True
        book.save()

        send_email_reject_book(book, reasons=request.POST['reasons'])

        messages.success(request, "La petición correspondiente al libro '{}' ha sido eliminada de su lista de peticiones aceptadas.".format(book.name))

    context = {
        "editor_view": editor_view,
        "deleted": deleted,
        "lists": lists,
        "thedate": thedate,
        "searchform": searchform,
        "list_count": list_count,
        "task_count": task_count,
        "all_lists": all_lists,
        "is_chief": is_chief
    }

    return render(request, "todo/accepted_petitions.html", context)
