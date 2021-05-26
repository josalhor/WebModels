from django.http import HttpResponse
from django.shortcuts import redirect

from todo.models import UserInfo
from todo.utils import staff_check, is_reader

def main(request) -> HttpResponse:
    if request.user.is_authenticated:

        if is_reader(request.user):
            return redirect("book_catalogue")
        elif staff_check(request.user):
            return redirect("home")

    else:
        return redirect("home")