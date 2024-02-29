from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    user = request.user
    return render(
        request,
        "index.html",
    )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    next_page = "index"

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class CustomLogout(SuccessMessageMixin, LogoutView):
    next_page = "index"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(self.request, _("You have been logged out."))
        return response
