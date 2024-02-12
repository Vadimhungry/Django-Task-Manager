from django.urls import path
from .views import IndexView, TaskCreate

urlpatterns = [
    path("", IndexView.as_view(), name="tasks_index"),
    path("create/", TaskCreate.as_view(), name="task_create")
]