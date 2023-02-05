from itertools import chain
from django.contrib.auth import get_user
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Review, Ticket


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = "listings/posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        context["title"] = "Your posts"
        context["posts"] = sorted(
            chain(
                Review.objects.order_by('-time_created').filter(user_id=user.id),
                Ticket.objects.order_by('-time_created').filter(user_id=user.id),
            ),
            key=lambda x: x.time_created,
            reverse=True
        )
        return context
