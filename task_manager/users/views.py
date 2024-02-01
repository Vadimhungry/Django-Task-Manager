from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthForm
from django.views import View
from task_manager.users.models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


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
        if form.is_valid():  # Если данные корректные, то сохраняем данные формы
            form.save()
            return redirect("users_index")  # Редирект на указанный маршрут
        # Если данные некорректные, то возвращаем человека обратно на страницу с заполненной формой
        return render(request, "users/create_user.html", {"form": form})


class UserUpdateFormView(View):
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
            return redirect("users_index")

        return render(
            request, "users/update_user.html", {"form": form, "user_id": user_id}
        )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    next_page = "index"
