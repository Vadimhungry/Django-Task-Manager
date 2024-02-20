from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    user = request.user
    return render(
        request,
        "index.html",
        context={
            "user": user,
        },
    )
