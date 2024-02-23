from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.views import View
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _
from django.contrib.auth.views import LogoutView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()[:15]
        return render(request, "users/index.html", context={"users": users})


class UserCreateFormView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, "users/create_user.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                self.request,
                _("The user has been successfully registered"),
                extra_tags="alert-success",
            )
            return redirect("user_login")
        return render(request, "users/create_user.html", {"form": form})


class UserUpdateFormView(UserPassesTestMixin, View):
    def test_func(self):
        current_user = self.request.user
        user_id = self.kwargs.get("user_id")
        if current_user.is_authenticated:
            if current_user.id == user_id or current_user.is_staff is True:
                return True
        return False

    def handle_no_permission(self):
        messages.warning(
            self.request, _("You do not have permission to modify another user.")
        )
        return redirect("users_index")

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserCreationForm(instance=user)
        return render(
            request, "users/update_user.html", {"form": form, "user_id": user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(self.request, _("The user has been successfully updated"))
            return redirect("users_index")

        return render(
            request, "users/update_user.html", {"form": form, "user_id": user_id}
        )


# class UserLoginView(LoginView):
#     form_class = CustomAuthForm
#     template_name = "users/login.html"
#     next_page = "index"
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, _("You are logged in"))
#         return response


class UserDeleteFormView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = CustomUser
    success_url = reverse_lazy("users_index")
    template_name = "users/delete_user.html"
    success_message = _("The user has been successfully deleted")

    def test_func(self):
        current_user = self.request.user
        user_id = self.kwargs.get("user_id")
        if current_user.id == user_id or current_user.is_staff is True:
            return True
        return False

    def get_object(self, queryset=None):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(CustomUser, id=user_id)

    def handle_no_permission(self):
        messages.warning(
            self.request, _("You do not have permission to modify another user.")
        )
        return redirect("users_index")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(
                self.request,
                _("Unable to delete the user because it is being used."),
            )
            return redirect("users_index")


class CustomLogout(SuccessMessageMixin, LogoutView):
    next_page = "index"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(self.request, _("You have been logged out."))
        return response
