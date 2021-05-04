import email.utils
import logging
import os
import time

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.template.loader import render_to_string

from todo.defaults import defaults
from todo.models import Attachment, Comment, Task, Writer, Editor, UserInfo, Designer

log = logging.getLogger(__name__)


def staff_check(user):
    """If TODO_STAFF_ONLY is set to True, limit view access to staff users only.
        # FIXME: More granular access control needed - see
        https://github.com/shacker/django-todo/issues/50
    """

    if defaults("TODO_STAFF_ONLY"):
        return user.is_staff
    else:
        # If unset or False, allow all logged in users
        return True

def chief_check(user):
    u = Editor.objects.filter().first()
    return u.chief


def user_can_read_book(book, user):
    author = Writer.objects.filter(user=user).first()
    editor = Editor.objects.filter(user=user).first()
    return (author != None and book.author == author) or \
           (editor != None and (book.editor == editor or editor.chief))
           
def user_can_design_book(book, task, user):
    editor = Editor.objects.filter(user=user).first()
    designer = Designer.objects.filter(user=user).first()
    return (editor != None and (book.editor == editor or editor.chief)) or \
           (designer != None and (task.designer == designer or designer.chief))

def user_can_read_task(task, user):
    if task.task_type == task.WRITING:
        return user_can_read_book(task.book_list, user)
    elif task.task_type == task.ILLUSTRATION or task.task_type == task.LAYOUT:
        return user_can_design_book(task.book_list, task, user)
    raise NotImplementedError('')


def todo_get_backend():
    mail_backends = getattr(settings, "TODO_MAIL_BACKENDS", None)
    if mail_backends is None:
        return None

    task_backend = mail_backends["mail-queue"]
    if task_backend is None:
        return None

    return task_backend

def todo_send_mail(user, task, subject, body, recip_list):
    references = ""

    backend = todo_get_backend()
    message_hash = hash((subject, body, user.pk, frozenset(recip_list), references))

    message_id = (
        # the task_id enables attaching back notification answers
        "<notif-{task_id}."
        # the message hash / epoch pair enables deduplication
        "{message_hash:x}."
        "{epoch}@django-todo>"
    ).format(
        task_id=task.pk,
        # avoid the -hexstring case (hashes can be negative)
        message_hash=abs(message_hash),
        epoch=int(time.time()),
    )

    # the thread message id is used as a common denominator between all
    # notifications for some task. This message doesn't actually exist,
    # it's just there to make threading possible
    thread_message_id = "<thread-{}@django-todo>".format(task.pk)
    references = "{} {}".format(references, thread_message_id)

    with backend() as connection:
        message = mail.EmailMessage(
            subject,
            body,
            None,
            recip_list,
            [],  # Bcc
            headers={
                **getattr(backend, "headers", {}),
                "Message-ID": message_id,
                "References": references,
                "In-reply-to": thread_message_id,
            },
            connection=connection,
        )
        message.send()


def send_notify_mail(new_task):
    if new_task.assigned_to == new_task.created_by:
        return

    current_site = Site.objects.get_current()
    subject = render_to_string("todo/email/assigned_subject.txt", {"task": new_task})
    body = render_to_string(
        "todo/email/assigned_task.txt", {"task": new_task, "site": current_site, "user": new_task.created_by.user}
    )

    recip_list = [new_task.assigned_to.user.email]
    todo_send_mail(new_task.created_by, new_task, subject, body, recip_list)


def send_email_to_thread_participants(task, msg_body, user, subject=None):
    current_site = Site.objects.get_current()
    email_subject = subject
    if not subject:
        subject = render_to_string("todo/email/assigned_subject.txt", {"task": task})

    user_info = UserInfo.objects.filter(user=user).first()
    email_body = render_to_string(
        "todo/email/newcomment_body.txt",
        {"task": task, "body": msg_body, "site": current_site, "user_info": user_info},
    )

    recip_list = get_thread_participants(task)

    todo_send_mail(user, task, email_subject, email_body, recip_list)

def get_thread_participants(task):
    commenters = Comment.objects.filter(task=task)
    recip_list = set(ca.author.user.email for ca in commenters if ca.author is not None)
    for related_user in (task.created_by, task.assigned_to):
        if related_user is not None:
            recip_list.add(related_user.user.email)
    return list(m for m in recip_list if m)


def toggle_task_completed(task_id: int) -> bool:
    try:
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return True

    except Task.DoesNotExist:
        log.info(f"Task {task_id} not found.")
        return False


def remove_attachment_file(attachment_id: int) -> bool:
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        if attachment.file:
            if os.path.isfile(attachment.file.path):
                os.remove(attachment.file.path)

        attachment.delete()
        return True

    except Attachment.DoesNotExist:
        log.info(f"Attachment {attachment_id} not found.")
        return False
