from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su contraseña ha sido correctamente actualizada')
            return redirect("todo:profile")
        else:
            no_errors = True
            for field in form:
                if(no_errors):
                    for error in field.errors:
                        messages.error(request, error)
                        no_errors = False
                else:
                    break
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'todo/change_password.html', {
        'form': form
    })