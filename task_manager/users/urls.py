from django.urls import path
from .views import (
    IndexView,
    UserCreate,
    UserUpdateFormView,
    UserDeleteFormView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="users_index"),
    path("create/", UserCreate.as_view(), name="user_create"),
    path(
        "<int:pk>/update/",
        UserUpdateFormView.as_view(),
        name="user_update"
    ),
    path(
        "<int:pk>/delete/",
        UserDeleteFormView.as_view(),
        name="delete_user"
    ),
]
