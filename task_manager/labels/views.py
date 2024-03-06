from django.views import View
from django.shortcuts import render, redirect
from .models import Label
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LabelCreateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _


class IndexView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()[:15]
        return render(request, "labels/index.html", context={"labels": labels})


class LabelCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("The label has been created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create label")
        context['action_url_name'] = "label_create"
        context['button_name'] = _("Create")
        return context


class LabelUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "update.html"
    success_message = _("The label has been successfully updated")
    success_url = reverse_lazy("labels_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context['title'] = _("Update label")
        context['action_url_name'] = "label_update"
        context['button_name'] = _("Update")
        return context


class LabelDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels_index")
    template_name = "delete.html"
    success_message = _("The label has been successfully deleted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete label")
        context['action_url_name'] = "label_delete"
        context['button_name'] = _("Yes, delete")
        return context

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
