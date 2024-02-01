from django.urls import path
from .views import IndexView, UserCreateFormView, UserUpdateFormView, UserLoginView, UserDeleteFormView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", IndexView.as_view(), name="users_index"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="users_index"), name="logout"),
    path("create/", UserCreateFormView.as_view(), name="user_create"),
    path("<int:user_id>/update/", UserUpdateFormView.as_view(), name="user_update"),
    path('<int:user_id>/delete/', UserDeleteFormView.as_view(), name='delete_user'),
]
