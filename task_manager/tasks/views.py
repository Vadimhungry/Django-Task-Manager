from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Task
from .forms import TaskCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .filters import TaskFilter
from django.utils.translation import gettext as _


class IndexView(LoginRequiredMixin, View):
    login_url = "user_login"

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()

        # Инициализация фильтра с исходным queryset и передача request
        filter = TaskFilter(request.GET, queryset=tasks, request=request)

        # Применение фильтра, если он был отправлен
        if "apply_filter" in request.GET:
            tasks = filter.qs

        return render(
            request, "tasks/index.html", context={"filter": filter, "tasks": tasks}
        )


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/create_task.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        messages.success(self.request, _("Task successfully created"))
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/update_task.html"
    success_message = _("Task successfully updated")
    success_url = reverse_lazy("tasks_index")

    def get_object(self, queryset=None):
        task_id = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=task_id)


class TaskDelete(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Task
    success_url = reverse_lazy("tasks_index")
    template_name = "tasks/delete_task.html"
    success_message = _("The task has been successfully deleted")

    def test_func(self):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return task.author == self.request.user

    def get_object(self, queryset=None):
        task_id = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=task_id)

    def handle_no_permission(self):
        messages.warning(self.request, _("The task can only be deleted by its author"))
        return HttpResponseRedirect(reverse("tasks_index"))


class TaskRead(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return render(request, "tasks/task.html", context={"task": task})
