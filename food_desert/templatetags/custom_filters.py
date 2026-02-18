from django import template

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Permet d'accéder à un dictionnaire par clé dans les templates Django."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''