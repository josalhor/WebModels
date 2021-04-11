from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from todo.models import Editor, Book, UserInfo, Writer

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

        u = User.objects.create_superuser('writer1@g.com', 'pass')
        UserInfo.objects.create(
            full_name="Writer1",
            user=u
        )
        w = Writer.objects.create(
            user=u,
        )
        b = Book.objects.create(
            name="Basic Book",
            author=w,
            editor=e,
            thematic='S'
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

        u = User.objects.create_superuser('writer2@g.com', 'pass')
        UserInfo.objects.create(
            full_name="Writer2",
            user=u
        )
        w = Writer.objects.create(
            user=u,
        )

        b = Book.objects.create(
            name="Not assigned Book",
            author=w,
            thematic='S',
            note="El otro día soñe que me despertaba y recogía el título del doble grado."
        )
