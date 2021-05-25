import datetime
import os

import bleach
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from project import templates

from todo.models import Book, PublishedBook

def book_catalogue(request) -> HttpResponse:
    books = PublishedBook.objects.all()
    success = True

    for book in books:
        book.pk = book.pk-1

    context = {
        "success": success,
        "published_books": books,
    }


    return render(request, "todo/main.html", context)