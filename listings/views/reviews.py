from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, CreateView, UpdateView
from lazy import lazy_success_url
from listings.forms import TicketEditForm
from listings.models import Review, Ticket


class NewReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ["headline", "rating", "body"]
    template_name = "listings/review_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            ticketid = int(self.request.GET["ticketid"])
            ticket = Ticket.objects.filter(pk=ticketid).first()
            context["ticket"] = ticket
        except Exception:
            context["ticket"] = None
        context["form_ticket"] = TicketEditForm(data=context["ticket"])
        return context

    def post(self, request, *args: str, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if "ticketid" in self.request.POST:
            ticket = Ticket.objects.get(pk=int(self.request.POST["ticketid"]))
        else:
            form_ticket = TicketEditForm(data=self.request.POST)
            ticket = form_ticket.save(commit=False)
            ticket.user = get_user(self.request)
        data = form.save(commit=False)
        data.user = get_user(self.request)
        data.ticket = ticket
        ticket.save()
        data.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ["headline", "rating", "body"]
    template_name = "listings/review_edit.html"
    pk_url_kwarg = "reviewid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.get_object().ticket
        if not context["ticket"]:
            try:
                ticketid = int(self.request.GET["ticketid"])
                ticket = Ticket.objects.filter(pk=ticketid).first()
                context["ticket"] = ticket
            except Exception:
                pass
        context["form_ticket"] = TicketEditForm(data=context["ticket"])
        context["back"] = self.get_success_url()
        return context

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "listings/ticket_review_delete.html"
    pk_url_kwarg = "reviewid"

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        image = self.object.image
        if not any(Ticket.objects.filter(image=image).exclude(pk=self.object.id)):
            image.delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")
