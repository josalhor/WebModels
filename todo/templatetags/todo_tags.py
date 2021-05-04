from django import template
from todo.models import Editor, UserInfo, Writer, Designer

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

@register.filter(name='get_full_name')
def get_full_name(u):
    return UserInfo.objects.filter(user=u).first().full_name
