from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthForm
from django.views import View
from task_manager.users.models import CustomUser
from django.contrib.auth.views import LoginView


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
            return redirect("user_login")
        return render(request, "users/create_user.html", {"form": form})


class UserUpdateFormView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get("user_id")
        if current_user.is_authenticated:
            if (current_user.id == user_id
                    or current_user.is_staff is True):
                user = get_object_or_404(CustomUser, id=user_id)
                form = CustomUserCreationForm(instance=user)
                return render(
                    request,
                    "users/update_user.html",
                    {"form": form, "user_id": user_id}
                )
        return redirect("users_index")

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users_index")

        return render(
            request,
            "users/update_user.html",
            {"form": form, "user_id": user_id}
        )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    next_page = "index"


class UserDeleteFormView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get("user_id")
        if current_user.is_authenticated:
            if (current_user.id == user_id
                    or current_user.is_staff is True):

                user = CustomUser.objects.get(id=user_id)
                return render(request, "users/delete_user.html", {"user": user})
            return redirect("users_index")
        return redirect("user_login")

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect("users_index")
