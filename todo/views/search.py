from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from todo.models import PublishedBook

def search(request):
    """Filters books by category and/or date and/or name.
    Parameters:
    request (request): Browser request for the view.
    """
    
    success = True
    books = []
    name = request.GET.get('n')

    if (name is None):
        return redirect('/')
    else:
        books = PublishedBook.objects.filter(book__name__icontains=name)

    if not books:
        success = False
        books = PublishedBook.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(books, 6) # Show 6 books per page
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'success': success,
        'books': books
    }

    return render(request, 'home.html', context)
