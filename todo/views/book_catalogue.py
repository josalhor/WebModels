import datetime
import os

import bleach
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from todo.models import Book, PublishedBook

def book_catalogue(request) -> HttpResponse:
    books = PublishedBook.objects

    context = {
        "published_books": books,
    }

    return render(request, "project/templates/main.html", context)