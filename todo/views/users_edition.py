from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from todo.forms import profileForm

from todo.models import Designer, Management, Writer, Editor
from todo.utils import staff_check

@login_required
@user_passes_test(staff_check)
@user_passes_test(is_management)
def users_edition(request, user_edit=None) -> HttpResponse:

    if request.method == 'POST':
        form = profileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    
    context = {
        "user": user_edit
    }

    return render(request, "todo/users_edition.html", context)
    
    
