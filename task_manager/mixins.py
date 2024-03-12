from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _



class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You are not logged in! Please log in.")
        )
        return redirect(reverse_lazy("user_login"))


class CanManageSelfObject(UserPassesTestMixin):
    no_permission_message = None
    no_permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.no_permission_message)
        return redirect(self.no_permission_url)


class CanManageCurrentTaskInstance(UserPassesTestMixin):
    no_permission_message = None
    no_permission_url = None

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.no_permission_message)
        return redirect(self.no_permission_url)