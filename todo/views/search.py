from django.http import HttpResponse
from django.shortcuts import render, redirect

from todo.models import PublishedBook, UserInfo

def search(request):
    """Filters books by category and/or date and/or name.
    Parameters:
    request (request): Browser request for the view.
    """
    
    success = True
    books = []
    words = request.GET.get('w')

    if (words == ""):
        return redirect('/')
    else:
        # By title
        books_bytitle = PublishedBook.objects.filter(title__icontains=words)
        # By author's name
        books_byauthor = PublishedBook.objects.filter(author_text__icontains=words)
        books = books_bytitle.union(books_byauthor)
        number_of_results = books.count

    if not books:
        success = False
        books = PublishedBook.objects.all()
    
    context = {
        "words": words,
        "success": success,
        "published_books": books,
        "number_of_results": number_of_results,
    }

    return render(request, "todo/main.html", context)
