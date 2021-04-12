from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from todo.defaults import defaults
from todo.forms import AddExternalBookForm, AddBookForm
from todo.models import Book, Editor, Writer, UserInfo
from todo.utils import staff_check
from django.contrib.auth.views import SetPasswordForm

def set_ft_pass(request, uuid) -> HttpResponse:
    user_info = UserInfo.objects.filter(reset_unique_id=uuid).first()
    if not user_info or user_info.used_reset:
        return render(request, "todo/password_reset_confirm.html", {'validlink': False})
    user = user_info.user
    
    if request.POST:
        set_password = SetPasswordForm(user, request.POST)
        if set_password.is_valid():
            set_password.save()
            user_info.used_reset = True
            user_info.save()
            return redirect("login")
        
    context = {
        'form': SetPasswordForm(user),
        'validlink': True
    }
    return render(request, "todo/password_reset_confirm.html", context)
    
