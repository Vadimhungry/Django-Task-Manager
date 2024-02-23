from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm
from django.contrib import messages
from django.utils.translation import gettext as _


def index(request):
    user = request.user
    return render(
        request,
        "index.html",
        context={
            "user": user,
        },
    )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    next_page = "index"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("You are logged in"))
        return response
