from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    user = request.user
    return render(request, 'index.html', context={
        'user': user,
    })