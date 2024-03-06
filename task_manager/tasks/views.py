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
from django.views.generic.base import ContextMixin
from django_filters.views import FilterView
from django.utils.translation import gettext as _


class IndexView(LoginRequiredMixin, FilterView, ContextMixin):
    login_url = "user_login"
    model = Task
    form_class = TaskCreateForm
    filterset_class = TaskFilter
    template_name = "tasks/index.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        messages.success(self.request, _("Task successfully created"))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create task")
        context['action_url_name'] = "task_create"
        return context


class TaskUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "update.html"
    success_message = _("Task successfully updated")
    success_url = reverse_lazy("tasks_index")

    def get_object(self, queryset=None):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(Task, id=task_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update task")
        context['action_url_name'] = "task_update"
        return context


class TaskDelete(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Task
    success_url = reverse_lazy("tasks_index")
    template_name = "delete.html"
    success_message = _("The task has been successfully deleted")

    def test_func(self):
        task_id = self.kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        return task.author == self.request.user

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Task, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete task")
        context['action_url_name'] = "task_delete"
        return context

    def handle_no_permission(self):
        messages.warning(
            self.request,
            _("The task can only be deleted by its author")
        )
        return HttpResponseRedirect(reverse("tasks_index"))


class TaskRead(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return render(request, "tasks/task.html", context={"task": task})
