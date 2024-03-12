from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.views import LogoutView


def index(request):
    return render(
        request,
        "index.html",
    )


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    next_page = "index"

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class CustomLogout(LogoutView):
    next_page = "index"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(self.request, _("You have been logged out."))
        return response
