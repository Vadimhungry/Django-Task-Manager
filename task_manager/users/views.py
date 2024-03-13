from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.mixins import (CanManageSelfObject, AuthRequiredMixin)
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect


class IndexView(ListView):
    model = CustomUser
    template_name = "users/index.html"


class UserCreate(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("user_login")
    success_message = _("The user has been successfully registered")
    extra_context = {
        'title': _("Registration"),
        'action_url_name': "user_create",
        'button_name': _("Register")
    }


class UserUpdateFormView(
    CanManageSelfObject, AuthRequiredMixin,
    SuccessMessageMixin, UpdateView
):
    template_name = "update.html"
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users_index")
    success_message = _("User changed successfully")
    no_permission_url = reverse_lazy("users_index")
    no_permission_message = _(
        "You do not have permission to change another user."
    )
    extra_context = {
        'title': _("Update user"),
        'action_url_name': "user_update",
        'button_name': _("Update")
    }


class UserDelete(
    CanManageSelfObject, AuthRequiredMixin,
    SuccessMessageMixin, DeleteView
):
    model = CustomUser
    success_url = reverse_lazy("users_index")
    template_name = "delete.html"
    success_message = _("The user has been successfully deleted")
    no_permission_url = reverse_lazy("users_index")
    no_permission_message = _(
        "You do not have permission to change another user."
    )
    extra_context = {
        'title': _("Delete user"),
        'action_url_name': "delete_user",
        'button_name': _("Yes, delete")
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(
                self.request,
                _("Cannot delete user because it is in use")
            )
            return redirect(reverse_lazy("users_index"))
