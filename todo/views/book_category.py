import datetime

import bleach
from django.db.models.fields import CharField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from project import templates

from todo.models import Book, PublishedBook

def book_category(request, category_id: str) -> HttpResponse:
    books = PublishedBook.objects.all()


    context = {
        "books": books,
        "category": category_id
    }


    return render(request, "todo/books_categories.html", context)