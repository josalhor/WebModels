from todo.utils import create_reader
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            create_reader(user)
            return redirect('todo:create_subscription')
        else:
            print(form.errors)
    return render(request, 'registration/signup.html')