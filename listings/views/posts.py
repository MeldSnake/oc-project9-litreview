from itertools import chain

from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Review, Ticket
from ..mixin.paginate import PaginateMixin


class PostsView(LoginRequiredMixin, PaginateMixin[Review | Ticket], TemplateView):
    template_name = "listings/posts.html"
    page_arg = "page"
    current_user = True

    def get_pagination_kwargs(self, page: int):
        data = super().get_pagination_kwargs(page)
        if not self.current_user:
            data["userid"] = self.kwargs["userid"]
        return data

    def get_paginated_objects(self):
        if self.current_user:
            user = get_user(self.request)
        else:
            user_model = get_user_model()
            user = user_model.objects.get(pk=self.kwargs["userid"])
        return sorted(
            chain(
                Ticket.objects.order_by('-time_created').filter(user_id=user.id),
                Review.objects.filter(user_id=user.id).order_by("-time_created"),
            ),
            key=lambda x: x.time_created,
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.current_user:
            user = get_user(self.request)
            context["title"] = "Your posts"
        else:
            user_model = get_user_model()
            user = user_model.objects.get(pk=self.kwargs["userid"])
            context["title"] = f"{user.get_username()} posts"
        context["user_view"] = user
        return context
