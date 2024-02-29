from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.utils import (PermissionUserMixin, AuthRequiredMixin,
                                ProtectedDeletionMixin)


class IndexView(ListView):
    model = CustomUser
    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.all()
        return context


class UserCreate(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy("user_login")

    def form_valid(self, form):
        messages.success(
            self.request,
            _("The user has been successfully registered"),
            extra_tags="alert-success",
        )
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserUpdateFormView(
    AuthRequiredMixin, PermissionUserMixin, SuccessMessageMixin, UpdateView
):
    template_name = "users/update_user.html"
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users_index")
    success_message = _("User changed successfully")
    no_permis_url = reverse_lazy("users_index")
    no_permis_message = _("You do not have permission to change another user.")


class UserDeleteFormView(
    AuthRequiredMixin, PermissionUserMixin,
    ProtectedDeletionMixin, SuccessMessageMixin, DeleteView
):
    model = CustomUser
    success_url = reverse_lazy("users_index")
    template_name = "users/delete_user.html"
    success_message = _("The user has been successfully deleted")
    no_permis_url = reverse_lazy("user_login")
    no_permis_message = _("You do not have permission to change another user.")

    no_protected_redirect_url = reverse_lazy("users_index")
    protected_message = _("Cannot delete user because it is in use")
