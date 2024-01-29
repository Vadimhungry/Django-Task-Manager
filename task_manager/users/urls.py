from django.urls import path
from task_manager.users import views
from .views import IndexView, UserCreateFormView

urlpatterns = [
    path('', IndexView.as_view(), name='users_index'),
    path('create/', UserCreateFormView.as_view(), name='user_create')
]