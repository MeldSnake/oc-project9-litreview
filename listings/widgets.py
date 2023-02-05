from django import forms
from django.utils.safestring import mark_safe


class TicketImagePreviewWidget(forms.widgets.ClearableFileInput):

    def render(self, name: str, value, attrs=None, renderer=None, **kwargs):
        origin = super().render(name, value, attrs, renderer, **kwargs)
        if value:
            preview = mark_safe(f"<picture class='ticket__cover'><img class='ticket__cover__image' src='{value.url}' alt='Cover'/></picture>")
            return f"{preview}{origin}"
        return origin
