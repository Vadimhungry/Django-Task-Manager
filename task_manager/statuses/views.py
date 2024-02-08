from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StatusCreateForm
from .models import Status
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


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
        return render(request, "statuses/index.html", context={"statuses": statuses})

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
            messages.success(self.request, "Статус успешно создан")
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
        current_user = request.user
        status_id = kwargs.get("status_id")

        status = get_object_or_404(Status, id=status_id)
        form = StatusCreateForm(instance=status)
        return render(
            request,
            "statuses/update_status.html",
            {"form": form, "status_id": status_id}
        )
        return redirect("ustatuses_index")

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("status_id")
        status = Status.objects.get(id=status_id)
        form = StatusCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Статус успешно изменен")
            return redirect("statuses_index")

        return render(
            request,
            "statuses/update_status.html",
            {"form": form, "status_id": status_id}
        )

class StatusDeleteFormView(UserPassesTestMixin, View):

    def test_func(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return True
        return False

    def handle_no_permission(self):
        return redirect("user_login")

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("status_id")

        status = Status.objects.get(id=status_id)
        return render(request, "statuses/delete_status.html", {"status": status})


    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("status_id")
        status = Status.objects.get(id=status_id)
        if status:
            status.delete()
            messages.success(self.request, "Статус успешно удален")
        return redirect("statuses_index")
