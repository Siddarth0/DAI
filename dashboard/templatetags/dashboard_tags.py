from django import template
import re, os

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


@register.filter
def file_extension(value):
    """Return the lowercase file extension of a FileField or string."""
    if not value:
        return ''
    name = getattr(value, 'name', '') or str(value)
    return os.path.splitext(name)[1].lower()


IMAGE_EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.gif'}

@register.filter
def is_image_extension(value):
    ext = file_extension(value)
    return ext in IMAGE_EXTENSIONS