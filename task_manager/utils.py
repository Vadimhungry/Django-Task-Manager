from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in! Please log in."))
            return redirect(reverse_lazy("user_login"))

        return super().dispatch(request, *args, **kwargs)


class PermissionUserMixin(UserPassesTestMixin):
    no_permis_message = None
    no_permis_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.no_permis_message)
        return redirect(self.no_permis_url)


class PermissionAuthorMixin(UserPassesTestMixin):
    no_permission_message = None
    no_permission_url = None

    def test_func(self):
        return self.get_object().author == self.request.user
        # current_user = self.request.user
        # user_id = self.kwargs.get("pk")
        # if current_user.id == user_id or current_user.is_staff is True:
        #     return True
        # return False

    def handle_no_permission(self):
        messages.warning(self.request, self.no_permission_message)
        return redirect(self.no_permission_url)


class ProtectedDeletionMixin:
    protected_message = None
    no_protected_redirect_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(self.request, self.protected_message)
            return redirect(self.no_protected_redirect_url)