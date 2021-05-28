from todo.templatetags.todo_tags import is_management
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from todo.models import UserInfo

@login_required
@user_passes_test(is_management)
def activate_user(request):
    
    if request.method == "POST":
        User = get_user_model()
        user = User.objects.filter(email=request.POST['activate-user']).first()
        user.is_active = True

        user.save()

        user = UserInfo.objects.filter(user=user).first()

        messages.success(request, "El usuario '{}' ha sido activado correctamente.".format(user.full_name))

    return redirect("todo:users_management")