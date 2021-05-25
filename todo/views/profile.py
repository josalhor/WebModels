
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

from todo.models import Reader, UserInfo

@login_required
def profile(request) -> HttpResponse:
    user_info = UserInfo.objects.filter(user=request.user).first()
    reader = Reader.objects.filter(user=request.user).first()
    context = {
        "user_info": user_info,
        "reader": reader,
    }

    return render(request, "todo/profile.html", context)
