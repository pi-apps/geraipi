import os
from typing import Any

from django import template

from frontend.view_helper import translater as tr

register = template.Library()


@register.simple_tag
def translater(to, page, value):
    to = to or "en"
    data = tr(to, page, value)
    return data


@register.filter
def env(key):
    return os.environ.get(key, False)


@register.filter(name="length_is")
def length_is(value: Any, length: str | int) -> bool:
    return len(value) == int(length)
