from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.utils import (IsAuthorizedUserMixin, AuthRequiredMixin,
                                ProtectedDeletionMixin)


class IndexView(ListView):
    model = CustomUser
    template_name = "users/index.html"
    context_object_name = "users"


class UserCreate(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("user_login")
    success_message = _("The user has been successfully registered")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Registration")
        context['action_url_name'] = "user_create"
        return context


class UserUpdateFormView(
    AuthRequiredMixin, IsAuthorizedUserMixin, SuccessMessageMixin, UpdateView
):
    template_name = "update.html"
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users_index")
    success_message = _("User changed successfully")
    no_permis_url = reverse_lazy("users_index")
    no_permis_message = _("You do not have permission to change another user.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update user")
        context['action_url_name'] = "user_update"
        return context


class UserDeleteFormView(
    AuthRequiredMixin, IsAuthorizedUserMixin,
    ProtectedDeletionMixin, SuccessMessageMixin, DeleteView
):
    model = CustomUser
    success_url = reverse_lazy("users_index")
    template_name = "delete.html"
    success_message = _("The user has been successfully deleted")
    no_permis_url = reverse_lazy("user_login")
    no_permis_message = _("You do not have permission to change another user.")
    no_protected_redirect_url = reverse_lazy("users_index")
    protected_message = _("Cannot delete user because it is in use")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete user")
        context['action_url_name'] = "delete_user"
        return context
