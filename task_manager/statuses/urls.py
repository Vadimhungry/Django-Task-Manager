from django.urls import path
from .views import IndexView, StatusCreateFormView, StatusUpdateFormView

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
    path(
        "<int:status_id>/update/",
        StatusUpdateFormView.as_view(),
        name="status_update"
    ),

]
