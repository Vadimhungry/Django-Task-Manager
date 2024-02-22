from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StatusCreateForm
from .models import Status
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import DeleteView
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


class StatusCreateFormView(UserPassesTestMixin, View):
    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        form = StatusCreateForm()
        return render(request, "statuses/create_status.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, _("Status successfully created"))
            return redirect("statuses_index")
        return render(request, "statuses/create_status.html", {"form": form})


class StatusUpdateFormView(UserPassesTestMixin, View):
    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("status_id")

        status = get_object_or_404(Status, id=status_id)
        form = StatusCreateForm(instance=status)
        return render(
            request,
            "statuses/update_status.html",
            {"form": form, "status_id": status_id},
        )
        return redirect("statuses_index")

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("status_id")
        status = Status.objects.get(id=status_id)
        form = StatusCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(self.request, _("Status successfully updated"))
            return redirect("statuses_index")

        return render(
            request,
            "statuses/update_status.html",
            {"form": form, "status_id": status_id},
        )


class StatusDeleteFormView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Status
    success_url = reverse_lazy("statuses_index")
    template_name = "statuses/delete_status.html"
    success_message = _("Status successfully deleted")

    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def get_object(self, queryset=None):
        status_id = self.kwargs.get("status_id")
        return get_object_or_404(Status, id=status_id)

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
