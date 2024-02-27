from django import template

from frontend.view_helper import translater as tr

register = template.Library()


@register.simple_tag
def translater(to, page, value):
    to = to or "en"
    data = tr(to, page, value)
    return data
