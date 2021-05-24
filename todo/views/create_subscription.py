import datetime
import os

import bleach
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from todo.defaults import defaults
from todo.models import UserInfo, Reader
from todo.forms import PaymentSubscriptionForm
from todo.utils

@login_required
def create_subscription(request) -> HttpResponse:
    user_email = request.user
    reader = Reader.objects.filter(user=user.email).first()
    
    if request.POST:
        form = PaymentSubscriptionForm(request.POST)
        
        if form.is_valid():
            reader = form.save(commit=False)
            reader.user = reader

            messages.success(request, "La subscripción ha sido correctamente creada.")
            email_body = render_to_string(
                "todo/email/created_subscription.txt", {"reader": reader}
            )

            send_mail(
                "Subcripción creada",
                email_body,
                None,
                [reader.user.email],
                fail_silently=False,
            )
    else:
        print(form.errors)
        messages.error(request, "Lo sentimos, la subscripción no ha podido ser creada.")
        return redirect(request.path)
            
    return redirect("")
    
    context = {
        'reader': reader,
        'payment_subcription_form': PaymentSubscriptionForm(),
    }
    return render(request, "todo/create_subscription.html", context)
