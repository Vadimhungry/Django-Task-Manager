from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StatusCreateForm
from .models import Status
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _


class IndexView(UserPassesTestMixin, View):
    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()[:15]
        return render(
            request,
            "statuses/index.html",
            context={"statuses": statuses}
        )


class StatusCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("statuses_index")
    success_message = _("Status successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'title': _("Create status"),
            'action_url_name': "status_create",
            'button_name': _("Create")
        }
        context.update(extra_context)
        return context


class StatusUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "update.html"
    success_message = _("Status successfully updated")
    success_url = reverse_lazy("statuses_index")

    def handle_no_permission(self):
        return redirect("user_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'title': _("Update status"),
            'action_url_name': "status_update",
            'button_name': _("Update")
        }
        context.update(extra_context)
        return context


class StatusDelete(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Status
    success_url = reverse_lazy("statuses_index")
    template_name = "delete.html"
    success_message = _("Status successfully deleted")

    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def get_object(self, queryset=None):
        status_id = self.kwargs.get("pk")
        return get_object_or_404(Status, id=status_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'title': _("Delete status"),
            'action_url_name': "delete_status",
            'button_name': _("Yes, delete")
        }
        context.update(extra_context)
        return context

    def handle_no_permission(self):
        return redirect("user_login")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(
                self.request,
                _("Unable to delete the status because it is in use")
            )
            return redirect("statuses_index")
