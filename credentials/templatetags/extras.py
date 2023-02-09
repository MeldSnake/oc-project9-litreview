from datetime import datetime
from django import template
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

MINUTE = 60
HOUR = 3600
DAY = 86400

register = template.Library()


@register.filter
def times(value):
    return range(value)


@register.filter
def sub(value, second):
    return value - second


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def short_date(value: datetime):
    diff_seconds = (timezone.now() - value).total_seconds()
    if diff_seconds < MINUTE:
        return f"{int(diff_seconds)} second{'s' if diff_seconds > 0 else ''} ago"
    if diff_seconds < HOUR:
        minutes = int(diff_seconds//MINUTE)
        return f"{minutes} minute{'s' if minutes > 0 else ''} ago"
    if diff_seconds < DAY:
        hours = int(diff_seconds//HOUR)
        return f"{hours} hour{'s' if hours > 0 else ''} ago"
    return value.strftime("%d %b %y à %Hh%M")


@register.simple_tag(takes_context=True)
def user_case(context, user: AbstractBaseUser | AnonymousUser):
    request = context.get("request")
    if request.user == user:
        return "You"
    return user.get_username()


@register.filter
def split(value: str, sep: str | None = None):
    return value.split(sep)
