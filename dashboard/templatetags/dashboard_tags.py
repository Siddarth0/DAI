from django import template
import re

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')


@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces in a string."""
    return value.replace('_', ' ')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def snake_to_title(value):
    if not isinstance(value, str):
        return value

    # Handle both snake_case and PascalCase
    value = value.replace('_', ' ')
    value = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', value)
    return value.title()