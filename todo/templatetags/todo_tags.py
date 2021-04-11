from django import template
from todo.models import Editor

register = template.Library()

@register.filter(name='is_chief_editor')
def is_chief_editor(u):
    return Editor.objects.filter(user=u, chief=True).first() is not None
