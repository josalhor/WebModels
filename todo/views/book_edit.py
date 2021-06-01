from todo.utils import can_covert_to_epub, convert_to_epub
from django.contrib import messages
from todo.defaults import defaults
from todo.forms import PublishedBookForm
from todo.models import PublishedBook, Book
from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

@login_required
@user_passes_test(is_management)
def book_edit(request, book_id: int) -> HttpResponse:
    published_book = get_object_or_404(PublishedBook, pk=book_id)

    if request.POST:
        form = PublishedBookForm(request.POST)

        if form.is_valid():
            # Handle uploaded files
            if request.FILES.get("attachment_file_input"):
                file = request.FILES.get("attachment_file_input")

                if file.size > defaults("TODO_MAXIMUM_ATTACHMENT_SIZE"):
                    messages.error(request, f"El archivo excede el tamaño máximo permitido.")
                    return redirect(request.path)

                published_book.final_version = file
            
            if request.FILES.get("attachment_image_input"):
                published_book.related_image = request.FILES.get("attachment_image_input")

            published_book.title = request.POST.get("title")
            published_book.book.description = request.POST.get("description")
            published_book.author_text = request.POST.get("author")
            published_book.book.completed = True
            published_book.book.save()
            published_book.save()
            if can_covert_to_epub():
                published_book.final_version_epub = convert_to_epub(published_book.final_version.path)
                published_book.save()

            messages.success(request, "¡Perfecto! Los parámetros se han modificado correctamente.")
            
        else:
            print(form.errors)
            messages.error(request, "Lo sentimos, el libro no ha podido editarse.")
            return redirect(request.path)
            
        return redirect("todo:book_detail", book_id=published_book.book.id)

    context = {
        'book': published_book,
        'edit_book_form': PublishedBookForm()
    }

    return render(request, "todo/book_edit.html", context)