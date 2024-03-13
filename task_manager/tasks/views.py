from .models import Task
from .forms import TaskCreateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .filters import TaskFilter
from django.views.generic.base import ContextMixin
from django_filters.views import FilterView
from django.utils.translation import gettext as _
from task_manager.mixins import CanManageCurrentTaskInstance
from django.views.generic import DetailView
from task_manager.mixins import AuthRequiredMixin


class IndexView(AuthRequiredMixin, FilterView, ContextMixin):
    login_url = "user_login"
    model = Task
    form_class = TaskCreateForm
    filterset_class = TaskFilter
    template_name = "tasks/index.html"


class TaskCreate(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("tasks_index")
    success_message = _("Task successfully created")
    extra_context = {
        'title': _("Create task"),
        'action_url_name': "task_create",
        'button_name': _("Create")
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdate(SuccessMessageMixin, AuthRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "update.html"
    success_message = _("Task successfully updated")
    success_url = reverse_lazy("tasks_index")
    extra_context = {
        'title': _("Update task"),
        'action_url_name': "task_update",
        'button_name': _("Update")
    }


class TaskDelete(
    AuthRequiredMixin, SuccessMessageMixin,
    CanManageCurrentTaskInstance, DeleteView
):
    model = Task
    template_name = "delete.html"

    success_url = reverse_lazy("tasks_index")
    no_permission_url = reverse_lazy("tasks_index")

    success_message = _("The task has been successfully deleted")
    no_permission_message = _("The task can only be deleted by its author")

    extra_context = {
        'title': _("Delete task"),
        'action_url_name': "task_delete",
        'button_name': _("Yes, delete")
    }


class TaskRead(AuthRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task.html"
