from django import template
from todo.models import Editor, UserInfo, Writer, Designer, Book, Reader

register = template.Library()

@register.filter(name='can_see_not_accepted')
def can_see_not_accepted(u):
    # Chief editor or writer
    if Editor.objects.filter(user=u, chief=True).first() is not None:
        return True
    return Writer.objects.filter(user=u).first() is not None

@register.filter(name='is_graphic_designer')
def is_graphic_designer(u):
    return Designer.objects.filter(user=u).first() is not None

@register.filter(name='is_editor')
def is_editor(u):
    return Editor.objects.filter(user=u).first() is not None

@register.filter(name='is_chief_designer')
def is_chief_designer(u):
    return Designer.objects.filter(user=u, chief=True).first() is not None

@register.filter(name='is_subscribed')
def is_subscribed(u):
    if not u.is_authenticated:
        return False
    return Reader.objects.filter(user=u, subscribed=True).first() is not None

@register.filter(name='get_full_name')
def get_full_name(u):
    return UserInfo.objects.filter(user=u).first().full_name

@register.filter(name='get_book_categories')
def get_book_categories(dummy):
    l = list(
        map(
            lambda x: x[1],
            Book.THEMATIC
        )
    )
    return l

@register.filter(name='is_staff')
def is_staff(u):
    return u.is_authenticated and \
        (
            is_graphic_designer(u) or 
            is_editor(u)
        )