from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from todo.models import Book, PublishedBook, Reader
from todo.utils import user_can_read_book

from todo.models import UserInfo
from todo.utils import is_reader

def download_book(request, book_id, format):
    book = get_object_or_404(Book, pk=book_id)
    if not request.user.is_authenticated:
        return redirect('login')
    if not is_reader(request.user):
        raise PermissionDenied
    
    reader = Reader.objects.filter(user=request.user).first()
    if not reader.subscribed:
        return redirect('todo:create_subscription')

    pb = PublishedBook.objects.filter(book=book).first()

    if format == "epub":
        return redirect(pb.final_version_epub.url)
    else:
        return redirect(pb.final_version.url)
