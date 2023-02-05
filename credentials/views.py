from django.views.generic import FormView
from django.contrib.auth import login
from .forms import RegisterForm
from lazy import lazy_success_url


class RegisterView(FormView):
    template_name = "credentials/register.html"
    form_class = RegisterForm
    success_url = "home-user"

    def get_success_url(self) -> str:
        return lazy_success_url(
            self.request.GET.get("next"),
            super().get_success_url(),
        )

    def form_valid(self, form: RegisterForm):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
