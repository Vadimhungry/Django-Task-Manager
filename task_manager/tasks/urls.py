from django.urls import path
from .views import IndexView, TaskRead, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path("", IndexView.as_view(), name="tasks_index"),
    path("create/", TaskCreate.as_view(), name="task_create"),
    path("<int:pk>/update/", TaskUpdate.as_view(), name="task_update"),
    path("<int:pk>/delete/", TaskDelete.as_view(), name="task_delete"),
    path("<int:pk>/", TaskRead.as_view(), name="task"),
]
