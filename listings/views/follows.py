from django.contrib.auth import get_user, get_user_model
from django.http import HttpRequest
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from listings.forms import AddFollower
from ..models import UserFollows
from lazy import lazy_success_url


class FollowsView(LoginRequiredMixin, TemplateView):
    template_name = "listings/follows.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        context["title"] = "Follows"
        context["add_follower_form"] = AddFollower
        context["users_followed"] = [x.followed_user for x in user.following.all()]
        context["users_follower"] = [x.user for x in user.followed_by.all()]
        return context


class FollowAddNameView(LoginRequiredMixin, FormView):
    pattern_name = "follow-list"
    form_class = AddFollower

    def get_success_url(self) -> str:
        return lazy_success_url(self.pattern_name)

    def form_valid(self, form: AddFollower):
        user = get_user(self.request)
        user_model = get_user_model()
        suser = user_model.objects.filter(username=form.cleaned_data['username']).first()
        if suser is None:
            form.add_error("username", "User not found")
        else:
            userfollow = UserFollows.objects.filter(user_id=user.id, followed_user_id=suser.id).first()
            if userfollow is None:
                UserFollows(user=user, followed_user=suser).save()
        return super().form_valid(form)


class FollowAddIdView(LoginRequiredMixin, RedirectView):
    pattern_name = "follow-list"

    def get(self, request: HttpRequest, *args, **kwargs):
        userid = int(self.kwargs["userid"])
        if userid > 0:
            user = get_user(self.request)
            user_model = get_user_model()
            suser = user_model.objects.filter(pk=userid)
            # Check that user does exists
            if suser is not None:
                # Check if user is already following the requested user.
                userfollow = user.following.filter(user_id=user.id, followed_user_id=suser.id).first()
                if userfollow is not None:
                    UserFollows(user=user, followed_user=suser).save()
        return super().get(request, *args, **kwargs)


class FollowDeleteView(LoginRequiredMixin, RedirectView):
    pattern_name = "follow-list"

    def get_redirect_url(self, *args, **kwargs) -> str:
        return lazy_success_url(self.pattern_name)

    def get(self, request: HttpRequest, *args, **kwargs):
        userid = int(self.kwargs["userid"])
        user = get_user(self.request)
        if userid > 0:
            userfollow = user.following.filter(user_id=user.id, followed_user_id=userid).first()
            if userfollow is not None:
                userfollow.delete()
        return super().get(request, *args, **kwargs)
