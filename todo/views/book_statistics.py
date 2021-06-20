from todo.models import PublishedBook, Book, RecordedDownload
from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

@login_required
@user_passes_test(is_management)
def book_statistics(request, book_id) -> HttpResponse:
    if not is_management(request.user):
        raise PermissionDenied
    book = get_object_or_404(Book, pk=book_id)
    get_stats = lambda: RecordedDownload.objects.filter(book=book)
    recordings = get_stats().order_by('download_date')
    pdf_recordings = get_stats().filter(download_type=RecordedDownload.PDF).count()
    epub_recordings = get_stats().filter(download_type=RecordedDownload.EPUB).count()

    print(pdf_recordings, epub_recordings)
    context = {
        "book": book,
        "recordings": recordings,
        "number_downloads": recordings.count,
        "pdf_downloads": pdf_recordings,
        "epub_downloads": epub_recordings,
    }

    return render(request, "todo/book_statistics.html", context)
