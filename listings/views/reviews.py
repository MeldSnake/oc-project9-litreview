from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, CreateView, UpdateView
from lazy import lazy_success_url
from listings.forms import ReviewEditForm, TicketEditForm
from listings.models import Review, Ticket


class NewReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewEditForm
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
        form_review = self.get_form()
        if "ticketid" in request.POST:
            form_ticket = None
        else:
            form_ticket = TicketEditForm(data=self.request.POST, files=self.request.FILES)
        if all([form_review.is_valid(), form_ticket is None or form_ticket.is_valid()]):
            return self.form_valid(form_review, form_ticket)
        else:
            return self.form_invalid(form_review)

    def form_valid(self, form, form_ticket=None):
        if form_ticket is None:
            ticket = Ticket.objects.get(pk=int(self.request.POST["ticketid"]))
        else:
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
    form_class = ReviewEditForm
    template_name = "listings/review_edit.html"
    pk_url_kwarg = "reviewid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        review = self.get_object()
        context["ticket"] = review.ticket
        context["forbidden"] = user != review.user
        if context["forbidden"]:
            if not context["ticket"]:
                try:
                    ticketid = int(self.request.GET["ticketid"])
                    ticket = Ticket.objects.filter(pk=ticketid).first()
                    context["ticket"] = ticket
                except Exception:
                    pass
            context["form_ticket"] = TicketEditForm(data=context["ticket"])
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
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return lazy_success_url("home-user")
