
from django.urls import NoReverseMatch, reverse


def lazy_success_url(*urls: str | None):
    i = 0
    while len(urls) != i:
        next_url = urls[i]
        if next_url:
            if hasattr(next_url, "get_absolute_url"):
                return next_url.get_absolute_url()
            if isinstance(next_url, str) and next_url.startswith(("./", "../")):
                return next_url
            try:
                return reverse(next_url)
            except NoReverseMatch:
                if callable(next_url):
                    raise
                if "/" not in next_url and "." not in next_url:
                    raise
            return next_url
        i += 1
