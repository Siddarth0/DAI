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
def snake_to_title(snake_str):
    # Replace underscores with spaces and capitalize each word
    return re.sub(r'_+', ' ', snake_str).title()