from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
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
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("The label has been created successfully")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/update_label.html"
    success_message = _("The label has been successfully updated")
    success_url = reverse_lazy("labels_index")

    def get_object(self, queryset=None):
        label_id = self.kwargs.get("label_id")
        return get_object_or_404(Label, id=label_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label_id"] = self.kwargs["label_id"]
        return context


class LabelDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("labels_index")
    template_name = "labels/delete_label.html"
    success_message = _("The label has been successfully deleted")

    def get_object(self, queryset=None):
        label_id = self.kwargs.get("label_id")
        return get_object_or_404(Label, id=label_id)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        connected_task_exist = self.object.task_set.exists()
        if connected_task_exist:
            messages.warning(
                request, _("Unable to delete the label because it is in use")
            )
            return redirect(reverse_lazy("labels_index"))
        else:
            success_url = self.get_success_url()
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(success_url)
