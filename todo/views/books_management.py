from todo.models import PublishedBook
from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from todo.utils import staff_check

@login_required
@user_passes_test(staff_check)
@user_passes_test(is_management)
def books_management(request) -> HttpResponse:
    books = PublishedBook.objects.all()

    context = {
        "books": books,
    }

    return render(request, "todo/books_management.html", context)
