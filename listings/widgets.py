from django import forms


class TicketImagePreviewWidget(forms.widgets.ClearableFileInput):

    template_name = "image_form.html"
