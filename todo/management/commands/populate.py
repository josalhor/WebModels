from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from todo.models import Editor, Book, UserInfo, Writer, Designer, Task 
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        u1 = User.objects.create_superuser('josep@g.com', 'pass')
        UserInfo.objects.create(
            full_name="JosepAdminEditor",
            user=u1
        )
        e1 = Editor.objects.create(
            user=u1,
            chief=True
        )

        u = User.objects.create_user('anna@g.com', 'pass')
        UserInfo.objects.create(
            full_name="AnnaEditor",
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

        u = User.objects.create_user('balma@g.com', 'pass')
        UserInfo.objects.create(
            full_name="BalmaChiefEditor",
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

        b2 = Book.objects.create(
            name="Not assigned Book",
            author=w,
            thematic='S',
            description="El otro día soñe que me despertaba y recogía el título del doble grado."
        )

        u = User.objects.create_user('chief.d@g.com', 'pass')
        UserInfo.objects.create(
            full_name="ChiefDesigner",
            user=u
        )
        d = Designer.objects.create(
            user=u,
            chief=True
        )

        u = User.objects.create_user('designer@g.com', 'pass')
        UserInfo.objects.create(
            full_name="Designer",
            user=u
        )
        d = Designer.objects.create(
            user=u,
            chief=False
        )
        t = Task.objects.create(
            title="DesignTask",
            book=b,
            task_type='I',
            created_by=e1,
            due_date=datetime.datetime(2022, 5, 14)
        )
