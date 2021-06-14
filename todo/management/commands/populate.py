from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from todo.models import Editor, Book, UserInfo, Writer, Designer, Task, PublishedBook, Management
from todo.utils import create_reader, try_add_epub_version
import datetime
from todo import static
from shutil import copyfile
from django.conf import settings
import os
from pathlib import Path


def move_to_media(path):
    name = os.path.basename(path)
    new_path = settings.MEDIA_ROOT + f'/default_copy_media/{name}'
    Path(new_path).parent.mkdir(parents=True, exist_ok=True)
    copyfile(path, new_path)
    return os.path.relpath(new_path, settings.MEDIA_ROOT)

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
            thematic='S',
        )

        pb = PublishedBook.objects.create(
            book= Book.objects.create(
                name="Published Book",
                author=w,
                editor=e,
                completed=True,
                description="When Justice Wynn slips into a coma, his law clerk, Avery Keene, must unravel the clues of a controversial case.",
                thematic=Book.TYPE_SCARE
            ),
            title="While Justice Sleeps",
            author_text="Stacey Abrams",
            related_image=move_to_media("todo/static/portada_libro.jpg"),
            final_version=move_to_media("todo/static/sample_book.pdf")
        )

        try_add_epub_version(pb)

        pb = PublishedBook.objects.create(
            book= Book.objects.create(
                name="The abandoned clunker",
                author=w,
                editor=e,
                completed=True,
                description="When Justice Wynn slips into a coma, his law clerk, Avery Keene, must unravel the clues of a controversial case.",
                thematic=Book.TYPE_ADVENTURE
            ),
            title="The abandoned clunker",
            author_text="THEODORE ASH",
            related_image=move_to_media("todo/static/portada_libro2.jpg"),
            final_version=move_to_media("todo/static/sample_book.pdf")
        )

        try_add_epub_version(pb)

        pb = PublishedBook.objects.create(
            book= Book.objects.create(
                name="El mundo contra el más allá",
                author=w,
                editor=e,
                completed=True,
                description="When Justice Wynn slips into a coma, his law clerk, Avery Keene, must unravel the clues of a controversial case.",
                thematic=Book.TYPE_FANTASY
            ),
            title="El mundo contra el más allá",
            author_text="Juan Ponce",
            related_image=move_to_media("todo/static/portada_libro3.jpg"),
            final_version=move_to_media("todo/static/sample_book.pdf")
        )

        try_add_epub_version(pb)

        u = User.objects.create_user('balma@g.com', 'pass')
        UserInfo.objects.create(
            full_name="BalmaChiefEditor",
            user=u
        )

        e = Editor.objects.create(
            user=u,
            chief=True
        )

        u = User.objects.create_user('manager@g.com', 'pass')
        UserInfo.objects.create(
            full_name="ManagerIT",
            user=u
        )

        m = Management.objects.create(
            user=u,
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

        u = User.objects.create_user('reader@g.com', 'pass')
        create_reader(u)
