from django.shortcuts import render



def index(request):
    user = request.user
    return render(
        request,
        "index.html",
        context={
            "user": user,
        },
    )
