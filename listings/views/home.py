from itertools import chain
from django.db.models import Q
from django.contrib.auth import get_user
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Review, Ticket
from ..mixin.paginate import PaginateMixin


class HomeView(LoginRequiredMixin, PaginateMixin[Ticket | Review], TemplateView):
    template_name = "listings/home.html"
    page_arg = "page"

    def get_paginated_objects(self):
        user = get_user(self.request)
        followed_users = [x.followed_user.id for x in user.following.all()]
        followed_users.append(user.id)
        return sorted(
            chain(
                Ticket.objects.filter(user_id__in=followed_users).order_by("-time_created"),
                Review.objects.filter(
                    Q(ticket__user_id=user.id)
                    | Q(user_id__in=followed_users)
                ).order_by("-time_created"),
            ),
            key=lambda x: x.time_created,
            reverse=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Flux"
        return context
