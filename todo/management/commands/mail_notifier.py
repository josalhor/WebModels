from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from todo.models import Editor, Book, UserInfo, Task

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Print tasks that are due on the next 3 days

        tasks = Task.objects.filter(notified_due_date=False)

        for task in tasks:
            today = models.DateField(auto_now_add=True)
            notification_due_date = today + datetime.timedelta(days=3)
            if task.due_date = notification_due_date:
                print(task)
                # Josep's mail code

                task.notified_due_date=True


