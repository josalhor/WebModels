from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from todo.models import UserInfo, PublishedBook

@login_required
@user_passes_test(is_management)
def activate_book(request):
    
    if request.method == "POST":
        book = PublishedBook.objects.filter(pk=request.POST['activate-book']).first()
        book.disabled = False

        book.save()

        messages.success(request, "El libro '{}' ha sido activado correctamente.".format(book.title))

    return redirect("todo:books_management")