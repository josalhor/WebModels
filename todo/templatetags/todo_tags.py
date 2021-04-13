from django import template
from todo.models import Editor, UserInfo

register = template.Library()

@register.filter(name='is_chief_editor')
def is_chief_editor(u):
    return Editor.objects.filter(user=u, chief=True).first() is not None

@register.filter(name='get_full_name')
def get_full_name(u):
    return UserInfo.objects.filter(user=u).first().full_name
