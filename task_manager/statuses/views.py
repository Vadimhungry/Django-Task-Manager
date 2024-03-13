from django.shortcuts import redirect
from .forms import StatusCreateForm
from .models import Status
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _
from task_manager.mixins import AuthRequiredMixin


class IndexView(AuthRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"


class StatusCreate(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("statuses_index")
    success_message = _("Status successfully created")
    extra_context = {
        'title': _("Create status"),
        'action_url_name': "status_create",
        'button_name': _("Create")
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusUpdate(SuccessMessageMixin, AuthRequiredMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "update.html"
    success_message = _("Status successfully updated")
    success_url = reverse_lazy("statuses_index")
    extra_context = {
        'title': _("Update status"),
        'action_url_name': "status_update",
        'button_name': _("Update")
    }


class StatusDelete(
    SuccessMessageMixin, AuthRequiredMixin, DeleteView
):
    model = Status
    success_url = reverse_lazy("statuses_index")
    template_name = "delete.html"
    success_message = _("Status successfully deleted")
    extra_context = {
        'title': _("Delete status"),
        'action_url_name': "delete_status",
        'button_name': _("Yes, delete")
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(
                self.request,
                _("Unable to delete the status because it is in use")
            )
            return redirect("statuses_index")
