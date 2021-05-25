from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.template.loader import render_to_string

from todo.models import UserInfo, Reader
from todo.forms import PaymentSubscriptionForm

@login_required
def cancel_subscription(request) -> HttpResponse:
    reader = Reader.objects.filter(user=request.user).first()
    
    # Permissions: only readers can cancel a subscription
    if reader is None or reader.subscribed == False:
        raise PermissionDenied

    if request.POST:
        if request.POST.get('cancel'):
            reader.subscribed = False
            reader.save()
            messages.success(request, "La subscripción ha sido correctamente cancelada.")
            
            email_body = render_to_string(
                "todo/email/canceled_subscription.txt", {"reader": reader}
            )

            send_mail(
                "Subcripción cancelada",
                email_body,
                None,
                [reader.user.email],
                fail_silently=False,
            )

        return redirect("todo:profile")
    else:
        return render(request, "todo/cancel_subscription.html")
