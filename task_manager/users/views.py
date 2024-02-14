from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthForm
from django.views import View
from task_manager.users.models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.db.models.deletion import ProtectedError


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
                "Пользователь успешно зарегистрирован",
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
            self.request, "У вас нет прав для изменения другого пользователя."
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
            messages.success(self.request, "Пользователь успешно изменен")
            return redirect("users_index")

        return render(
            request, "users/update_user.html", {"form": form, "user_id": user_id}
        )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    next_page = "index"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response


class UserDeleteFormView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = CustomUser
    success_url = reverse_lazy("users_index")
    template_name = "users/delete_user.html"
    success_message = "Пользователь успешно удален"

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
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_index")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(
                self.request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect("users_index")

            # def get(self, request, *args, **kwargs):

    #     user_id = kwargs.get("user_id")
    #     user = CustomUser.objects.get(id=user_id)
    #     return render(request, "users/delete_user.html", {"user": user})
    #
    # def post(self, request, *args, **kwargs):
    #     user_id = kwargs.get("user_id")
    #     user = CustomUser.objects.get(id=user_id)
    #     if user:
    #         user.delete()
    #     return redirect("users_index")
