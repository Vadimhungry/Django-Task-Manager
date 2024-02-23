from django.urls import path
from .views import (
    IndexView,
    UserCreateFormView,
    UserUpdateFormView,
    UserDeleteFormView,
    CustomLogout,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", IndexView.as_view(), name="users_index"),
    # path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", CustomLogout.as_view(), name="logout"),
    path("create/", UserCreateFormView.as_view(), name="user_create"),
    path("<int:user_id>/update/", UserUpdateFormView.as_view(), name="user_update"),
    path("<int:user_id>/delete/", UserDeleteFormView.as_view(), name="delete_user"),
]
