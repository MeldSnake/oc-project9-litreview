"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from listings.views.home import HomeView
from listings.views.posts import PostsView
from listings.views.follows import FollowsView, FollowAddIdView, FollowDeleteView
from credentials.views import RegisterView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from listings.views.tickets import TicketDeleteView, NewTicketView, EditTicketView
from listings.views.reviews import ReviewDeleteView, NewReviewView, EditReviewView


class NotImplementedView(TemplateView):
    template_name = "notimplemented.html"
    title: str | None = None

    def __init__(self, title: str | None = None, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["content"] = "<p class='warning'>Not implemented yet</p>"
        # Data passed to functions are within self.args and self.kwargs
        # django.shortcuts.get_object_or_404
        if self.request.user.is_authenticated:
            context["extend"] = "base_logged.html"
        else:
            context["extend"] = "base.html"
        return context


urlpatterns = [
    path('admin/', admin.site.urls, name='admin-index'),

    # Authentication endpoints
    path('login/', LoginView.as_view(
            template_name="credentials/login.html",
            next_page="home-user",
            redirect_authenticated_user=True,
        ), name='login-user'),
    path('logout/', LogoutView.as_view(
            next_page="login-user"
        ), name='logout-user'),
    path('register/', RegisterView.as_view(
        ), name='register-user'),

    # Main pages endpoints
    path('', HomeView.as_view(
            page_url="home-user-page",
            limit=5,
        ), name='home-user'),
    path('<int:page>/', HomeView.as_view(
            page_url="home-user-page",
            limit=5,
        ), name='home-user-page'),
    path('follows/', FollowsView.as_view(
        ), name='follow-list'),
    path('posts/', PostsView.as_view(
            page_url="post-list-page",
        ), name='post-list'),
    path('posts/<int:page>/', PostsView.as_view(
            page_url="post-list-page",
        ), name='post-list-page'),

    # Tickets endpoints
    path('tickets/new/', NewTicketView.as_view(
        ), name='ticket-new'),
    path('tickets/<int:ticketid>/edit/', EditTicketView.as_view(
        ), name='ticket-edit'),
    path('tickets/<int:ticketid>/delete/', TicketDeleteView.as_view(
        ), name='ticket-delete'),

    # Reviews endpoints
    path('reviews/new/', NewReviewView.as_view(
        ), name='review-new'),
    path('reviews/<int:reviewid>/edit/', EditReviewView.as_view(
        ), name='review-edit'),
    path('reviews/<int:reviewid>/delete/', ReviewDeleteView.as_view(
        ), name='review-delete'),

    # Follows endpoints
    path('user/<int:userid>/posts/', PostsView.as_view(
            current_user=False,
            page_url="user-list-page",
            limit=5,
        ), name='user-list'),
    path('user/<int:userid>/posts/<int:page>/', PostsView.as_view(
            current_user=False,
            page_url="user-list-page",
            limit=5,
        ), name='user-list-page'),
    path('follows/<int:userid>/add/', FollowAddIdView.as_view(
        ), name='follow-add'),
    path('follows/<int:userid>/delete/', FollowDeleteView.as_view(
        ), name='follow-delete'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )