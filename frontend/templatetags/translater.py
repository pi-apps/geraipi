from django import template
import os

from frontend.view_helper import translater as tr

register = template.Library()


@register.simple_tag
def translater(to, page, value):
    to = to or "en"
    data = tr(to, page, value)
    return data


@register.simple_tag
def env(key):
    return os.environ.get(key, False)
