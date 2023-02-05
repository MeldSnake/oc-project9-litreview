from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, CreateView, UpdateView
from lazy import lazy_success_url
from listings.forms import TicketEditForm
from listings.models import Ticket


class NewTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ["title", "description", "image"]
    template_name = "listings/ticket_edit.html"

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = get_user(self.request)
        data.save()
        return super().form_valid(form)


class EditTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    # fields = ["title", "description", "image"]
    form_class = TicketEditForm
    template_name = "listings/ticket_edit.html"
    pk_url_kwarg = "ticketid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.filter(pk=int(self.kwargs["ticketid"])).first()
        context["ticket"] = ticket
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "listings/ticket_review_delete.html"
    pk_url_kwarg = "ticketid"

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")
