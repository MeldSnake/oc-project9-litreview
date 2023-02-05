from itertools import chain
from django.contrib.auth import get_user
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Review, Ticket


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "listings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        followed_users = [x.followed_user.id for x in user.following.all()]
        followed_users.append(user.id)
        context["title"] = "Flux"
        context["posts"] = sorted(
            chain(
                Review.objects.filter(user_id__in=followed_users).order_by("-time_created"),
                Ticket.objects.filter(user_id__in=followed_users).order_by("-time_created"),
            ),
            key=lambda x: x.time_created,
            reverse=True
        )
        return context
