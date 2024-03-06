from django.urls import path
from .views import (
    IndexView,
    StatusCreate,
    StatusUpdate,
    StatusDelete,
)

urlpatterns = [
    path("", IndexView.as_view(), name="statuses_index"),
    path("create/", StatusCreate.as_view(), name="status_create"),
    path(
        "<int:pk>/update/",
        StatusUpdate.as_view(),
        name="status_update"
    ),
    path(
        "<int:pk>/delete/",
        StatusDelete.as_view(),
        name="delete_status"
    ),
]
