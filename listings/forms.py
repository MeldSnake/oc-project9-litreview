from django import forms

from listings.widgets import TicketImagePreviewWidget
from .models import Review, Ticket


class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "rating", "body")


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            'image': TicketImagePreviewWidget()
        }


class AddFollower(forms.Form):
    # TODO Add validator to make sure that the user does exists and return an answer to the parent when possible
    username = forms.CharField(max_length=63, help_text="Enter a valid username")
