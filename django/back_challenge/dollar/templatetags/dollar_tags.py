from django import template

register = template.Library()


@register.filter(name='to_mxn')
def to_mxn(value):

    return f'{round(value, 2)} MXN'
