from todo.models import PublishedBook, Book
from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

@login_required
@user_passes_test(is_management)
def books_management(request) -> HttpResponse:
    books = PublishedBook.objects.all()
    active_books = PublishedBook.objects.filter(disabled = False)
    unactive_books = PublishedBook.objects.filter(disabled = True)


    context = {
        "books": books,
        "active_books": active_books,
        "unactive_books": unactive_books,
    }

    return render(request, "todo/books_management.html", context)
