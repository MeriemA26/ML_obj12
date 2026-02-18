from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie la valeur par arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def percentage(value):
    """Convertit un décimal en pourcentage avec 2 décimales."""
    try:
        return f"{float(value) * 100:.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def dict_get(dictionary, key):
    """Récupère une valeur d'un dictionnaire par clé."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''