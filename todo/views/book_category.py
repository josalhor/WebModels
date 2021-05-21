import datetime
import os

import bleach
from django.db.models.query import NamedValuesListIterable
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from todo.models import Book, PublishedBook

def book_category(request, book_id: int) -> HttpResponse:
    return NotImplementedError
    