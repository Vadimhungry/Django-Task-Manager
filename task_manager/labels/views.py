from django.shortcuts import redirect
from .models import Label
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LabelCreateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView
from task_manager.mixins import AuthRequiredMixin


class IndexView(AuthRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class LabelCreate(SuccessMessageMixin, AuthRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("The label has been created successfully")
    extra_context = {
        'title': _("Create label"),
        'action_url_name': "label_create",
        'button_name': _("Create")
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdate(SuccessMessageMixin, AuthRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "update.html"
    success_message = _("The label has been successfully updated")
    success_url = reverse_lazy("labels_index")
    extra_context = {
        'title': _("Update label"),
        'action_url_name': "label_update",
        'button_name': _("Update")
    }


class LabelDelete(SuccessMessageMixin, AuthRequiredMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels_index")
    template_name = "delete.html"
    success_message = _("The label has been successfully deleted")
    extra_context = {
        'title': _("Delete label"),
        'action_url_name': "label_delete",
        'button_name': _("Yes, delete")
    }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        connected_task_exist = self.object.task_set.exists()
        if connected_task_exist:
            messages.warning(
                request, _("Unable to delete the label because it is in use")
            )
            return redirect(reverse_lazy("labels_index"))
        else:
            return super().post(request, *args, **kwargs)
