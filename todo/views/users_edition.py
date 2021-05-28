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
def users_edition(request, list_slug, email) -> HttpResponse:

    if request.method == 'POST':
        form = profileForm(data=request.POST, instance=request.user) #should be user_edit
        if form.is_valid():
            form.save()
            return redirect('todo/users_management/'+list_slug)
        else:
            form = profileForm(instance=request.user) #should be user_edit
            args={'form': form}
            return render(request, 'todo/users_edition.html', args)
    
    context = {
        "user": request.user, #should be user_edit
        # "user_edit": user_edit
    }

    return render(request, "todo/users_edition.html", context)
    
    
