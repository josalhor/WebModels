import datetime
import os

import bleach
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from todo.models import Book, PublishedBook


def book_detail(request, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_id)
    published_book = PublishedBook.objects.filter(book=book).first()
    
    context = {
        'published_book' : published_book,
        'book': book
    }
    return render(request, "todo/book_detail.html", context)