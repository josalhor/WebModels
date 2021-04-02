from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from todo.models import Editor, Book, UserInfo

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        u = User.objects.create_superuser('admin@g.com', 'pass')
        UserInfo.objects.create(
            full_name="SuperAdminEditor",
            user=u
        )
        e = Editor.objects.create(
            user=u,
            chief=True
        )

        u = User.objects.create_user('basic@g.com', 'pass')
        UserInfo.objects.create(
            full_name="BasicEditor",
            user=u
        )
        e = Editor.objects.create(
            user=u,
            chief=False
        )
        b = Book.objects.create(
            name="Basic Book",
            editor=e
        )

        u = User.objects.create_user('chief@g.com', 'pass')
        UserInfo.objects.create(
            full_name="ChiefEditor",
            user=u
        )

        e = Editor.objects.create(
            user=u,
            chief=True
        )
