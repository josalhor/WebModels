from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render


@login_required
@user_passes_test(is_management)
def users_management(request) -> HttpResponse:
    section_list = {"Escritores":"writers", "Editores":"editors", "Disenyadores gràficos":"designers", "Responsables IT":"management"}

    context = {
        "section_list": section_list,
    }

    return render(request, "todo/users_management.html", context)
