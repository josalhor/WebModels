from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
import datetime
from todo.models import Editor, Book, UserInfo, Task

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Print tasks that are due on the next 3 days

        tasks = Task.objects.filter(completed=False, notified_due_date=False)
        for task in tasks:
            if task.due_date is None:
                continue
            notification_due_date = task.due_date - datetime.timedelta(days=3)
            if notification_due_date <= today:
                print(task.title)
                current_site = Site.objects.get_current()

                email_body = render_to_string(
                    "todo/email/task_remainder.txt",
                    {"task": task, "site": current_site},
                )

                send_mail(
                    'La tarea está a punto de finalizar',
                    email_body,
                    None,
                    [task.assigned_to.user.email],
                    fail_silently=False,
                )

                task.d_due_date = True
                task.save()


