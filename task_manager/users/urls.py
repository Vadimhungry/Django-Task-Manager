from django.urls import path, include
from task_manager.users import views
from .views import IndexView, UserCreateFormView, UserUpdateFormView, UserLoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", IndexView.as_view(), name="users_index"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("create/", UserCreateFormView.as_view(), name="user_create"),
    path("<int:user_id>/update/", UserUpdateFormView.as_view(), name="user_update"),
]
