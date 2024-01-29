from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.views import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # articles = Article.objects.all()[:15]
        return render(
            request,
            "users/index.html",
            context={
                "users": "USSSEEEERRRSSS"
            }
        )


class UserCreateFormView(View):

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'users/create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # Если данные корректные, то сохраняем данные формы
            form.save()
            return redirect('articles')  # Редирект на указанный маршрут
        # Если данные некорректные, то возвращаем человека обратно на страницу с заполненной формой
        return render(request, 'articles/create.html', {'form': form})