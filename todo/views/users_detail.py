from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from todo.models import Designer, Management, Writer, Editor
from todo.utils import chief_check, staff_check

@login_required
@user_passes_test(staff_check)
@user_passes_test(is_management)
def users_detail(request, list_slug=None) -> HttpResponse:
    
    # Which users to show on this list view?
    if list_slug == "editors":
        users = Editor.objects.all()
    elif list_slug == "designers":
        users = Designer.objects.all()
    elif list_slug == "writers":
        users = Writer.objects.all()
    elif list_slug == "management":
        users = Management.objects.all()

    # Additional filtering
    active_users = users.filter(user__is_active=True)
    unactive_users = users.filter(user__is_active=False)

    # ######################
    #  Add New User Form
    # ######################

    context = {
        "list_slug": list_slug,
        "active_users": active_users,
        "unactive_users":  unactive_users,
    }

    return render(request, "todo/users_detail.html", context)
