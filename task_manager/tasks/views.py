from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Task
from .forms import TaskCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
import time



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


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/create_task.html'  # Шаблон для отображения формы
    success_url = reverse_lazy('tasks_index')  # URL для перенаправления после успешного создания объекта

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно создана")
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks_index')

    def get_object(self, queryset=None):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(Task, id=task_id)


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_index')
    template_name = 'tasks/delete_task.html'
    def test_func(self):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        return task.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Задача успешно удалена")
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(Task, id=task_id)

