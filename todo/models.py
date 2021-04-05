from __future__ import unicode_literals

import datetime
import os
import textwrap

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import models as auth_models
from cuser.models import AbstractCUser
from django.db import DEFAULT_DB_ALIAS, models
from django.db.transaction import Atomic, get_connection
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from abc import ABC


def get_attachment_upload_dir(instance, filename):
    """Determine upload dir for task attachment files.
    """

    return "/".join(["tasks", "attachments", str(instance.task.id), filename])


class LockedAtomicTransaction(Atomic):
    """
    modified from https://stackoverflow.com/a/41831049
    this is needed for safely merging

    Does a atomic transaction, but also locks the entire table for any transactions, for the duration of this
    transaction. Although this is the only way to avoid concurrency issues in certain situations, it should be used with
    caution, since it has impacts on performance, for obvious reasons...
    """

    def __init__(self, *models, using=None, savepoint=None):
        if using is None:
            using = DEFAULT_DB_ALIAS
        super().__init__(using, savepoint)
        self.models = models

    def __enter__(self):
        super(LockedAtomicTransaction, self).__enter__()

        # Make sure not to lock, when sqlite is used, or you'll run into problems while running tests!!!
        if settings.DATABASES[self.using]["ENGINE"] != "django.db.backends.sqlite3":
            cursor = None
            try:
                cursor = get_connection(self.using).cursor()
                for model in self.models:
                    cursor.execute(
                        "LOCK TABLE {table_name}".format(table_name=model._meta.db_table)
                    )
            finally:
                if cursor and not cursor.closed:
                    cursor.close()

# Does this look repetitive to you?
# Then great! It looks repetitive to me too!

# The way Django works, this way of building the models
# is better for form handling.

class UserInfo(models.Model):
    full_name = models.CharField(max_length=150)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        null=False,
        on_delete=models.CASCADE,
        related_name='user_info'
    )

    def __str__(self):
        return str(self.full_name)

# This should be an ABC, but that interferes
# with the model's metaclass
class UserRole(models.Model):
    def __str__(self):
        return str(self.user.user_info)

class Writer(UserRole):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        null=False,
        on_delete=models.CASCADE
    )


class Editor(UserRole):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        null=False,
        on_delete=models.CASCADE
    )
    chief = models.BooleanField(default=False)

# These classes are not to be used in the first iteration of
# the app. However, modeling them helps us make better design decisions
# and prepare generic code :D

class Designer(UserRole):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        null=False,
        on_delete=models.CASCADE
    )
    chief = models.BooleanField(default=False)

class Reader(UserRole):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        null=False,
        on_delete=models.CASCADE
    )

class Book(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(default="", unique=True)
    author = models.ForeignKey(Writer, null=True, blank=True, on_delete=models.RESTRICT, related_name='book_author')
    editor = models.ForeignKey(Editor, null=True, blank=True, on_delete=models.CASCADE, related_name='book_editor')
    completed = models.BooleanField(default=False)
    note = models.TextField()

    TYPE_SCARE = 'S'
    TYPE_ADVENTURE = 'A'
    TYPE_FANTASY = 'F'

    THEMATIC = [
        (TYPE_SCARE, 'Miedo'),
        (TYPE_ADVENTURE, 'Aventura'),
        (TYPE_FANTASY, 'Fantasía'),
    ]

    thematic = models.CharField(
        max_length=2,
        choices=THEMATIC,
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Book, self).save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Books"


class Task(models.Model):

    WRITING = 'E'
    ILLUSTRATION = 'I'
    LAYOUT = 'M'

    TYPES_OF_TASK_CHOICES = [
        (WRITING, 'Escritura'),
        (ILLUSTRATION, 'Ilustración'),
        (LAYOUT, 'Maquetación'),
    ]

    title = models.CharField(max_length=140)
    book_list = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    task_type = models.CharField(
        max_length=2,
        choices=TYPES_OF_TASK_CHOICES,
        default=LAYOUT,
    )
    created_by = models.ForeignKey(
        Editor,
        null=True,
        blank=True,
        related_name="todo_created_by",
        on_delete=models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        UserInfo,
        blank=True,
        null=True,
        related_name="todo_assigned_to",
        on_delete=models.CASCADE,
    )
    note = models.TextField(default="")
    priority = models.PositiveIntegerField(blank=True, null=True)

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the Tasks's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo:task_detail", kwargs={"task_id": self.id})

    # Auto-set the Task creation / completed date
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    def merge_into(self, merge_target):
        if merge_target.pk == self.pk:
            raise ValueError("can't merge a task with self")

        # lock the comments to avoid concurrent additions of comments after the
        # update request. these comments would be irremediably lost because of
        # the cascade clause
        with LockedAtomicTransaction(Comment):
            Comment.objects.filter(task=self).update(task=merge_target)
            self.delete()

    class Meta:
        ordering = ["priority", "created_date"]


class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """

    author = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(default="")

    @property
    def author_text(self):
        return str(self.author)

    @property
    def snippet(self):
        body_snippet = textwrap.shorten(self.body, width=35, placeholder="...")
        # Define here rather than in __str__ so we can use it in the admin list_display
        return "{author} - {snippet}...".format(author=self.author_text, snippet=body_snippet)

    def __str__(self):
        return self.snippet


class Attachment(models.Model):
    """
    Defines a generic file attachment for use in M2M relation with Task.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_attachment_upload_dir, max_length=255)

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def __str__(self):
        return f"{self.task.id} - {self.file.name}"