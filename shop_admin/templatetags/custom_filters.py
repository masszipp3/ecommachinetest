from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def mul(value, arg):
    return round(value * arg,2)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)