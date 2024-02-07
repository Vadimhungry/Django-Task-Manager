from django.urls import path
from .views import IndexView, StatusCreateFormView

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="statuses_index"
    ),
    path(
        "create/",
        StatusCreateFormView.as_view(),
        name="status_create"
    ),

]
