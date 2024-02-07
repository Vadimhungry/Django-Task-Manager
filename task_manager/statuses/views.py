from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import StatusCreateForm
from .models import Status


class IndexView(View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()[:15]
        return render(request, "statuses/index.html", context={"statuses": statuses})

class StatusCreateFormView(View):

    def get(self, request, *args, **kwargs):
        form = StatusCreateForm()
        return render(request, "statuses/create_status.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("statuses_index")
        return render(request, "statuses/create_status.html", {"form": form})
