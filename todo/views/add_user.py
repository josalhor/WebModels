from project.forms import UserCreationForm
from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from todo.utils import create_designer, create_editor, create_manager, create_reader, create_writer
from django.contrib.auth import authenticate

from todo.models import Designer, Management, Writer, Editor

@login_required
@user_passes_test(is_management)
def add_user(request, list_slug=None) -> HttpResponse:
    if list_slug == "editors" or list_slug == "designers":
        chief_option = True
    else:
        chief_option = False
    
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            full_name = form.cleaned_data.get('full_name')
            chief = form.cleaned_data.get('chief')
            user = authenticate(email=email, password=password)
            if list_slug == "editors":
                create_editor(user, full_name, chief)
            elif list_slug == "designers":
                create_designer(user, full_name, chief)
            elif list_slug == "writers":
                create_writer(user, full_name)
            elif list_slug == "management":
                create_manager(user, full_name)
            return redirect("todo:users_detail", list_slug=list_slug)
        else:
            print(form.errors)
            no_errors = True
            for field in form:
                if(no_errors):
                    for error in field.errors:
                        messages.error(request, error)
                        no_errors = False
                else:
                    break
    
    context = {
        "list_slug": list_slug,
        "chief_option": chief_option,
    }

    return render(request, "todo/add_user.html", context)
