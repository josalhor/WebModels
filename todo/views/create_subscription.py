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

@login_required
def create_subscription(request) -> HttpResponse:
    reader = Reader.objects.filter(user=request.user).first()
    
    # Permissions: only readers can get a subscription
    if reader is None:
        raise PermissionDenied

    if request.POST:
        if reader.subscribed:
            messages.error(request, "Ya está subscrito a Bookiernes, S.A.")
            return redirect("home")

        form = PaymentSubscriptionForm(request.POST)
        
        if form.is_valid():
            item = form.save()
            reader.subscribed = True
            reader.credit_card = item
            reader.save()

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

            return redirect("book_catalogue")
            #TODO: should redirect to the reader's profile once we created

        else:
            print(form.errors)
    else:
        form = PaymentSubscriptionForm()
    
    context = {
        "payment_subcription_form": PaymentSubscriptionForm(),
    }

    return render(request, "todo/create_subscription.html", context)
