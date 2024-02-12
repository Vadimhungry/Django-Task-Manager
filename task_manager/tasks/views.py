from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task
from .forms import TaskCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class IndexView(View):

    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()[:15]
        return render(request, "tasks/index.html", context={"tasks": tasks})


class TaskCreate(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render(request, "tasks/create_task.html", {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        form.fields['author'] = request.user
        if form.is_valid():
            task = form.save(commit=False)
            # task.author = request.user  # Задаем текущего пользователя в качестве автора задачи
            task.save()
            messages.success(request, "Задача успешно создана")
            return redirect("tasks_index")
        return render(request, "tasks/create_task.html", {"form": form})