from django.http import HttpResponse
from django.shortcuts import redirect

from todo.models import UserInfo
from todo.utils import is_reader

def main(request) -> HttpResponse:
    if request.user.is_authenticated:

        if is_reader(request.user):
            return redirect("book_catalogue")
        else:
            return redirect("home")

    else:
        return redirect("book_catalogue")