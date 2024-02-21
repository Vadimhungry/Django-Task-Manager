from django.urls import path
from .views import IndexView, LabelCreate, LabelUpdate, LabelDelete

urlpatterns = [
    path("", IndexView.as_view(), name="labels_index"),
    path("create/", LabelCreate.as_view(), name="label_create"),
    path("<int:label_id>/update/", LabelUpdate.as_view(), name="label_update"),
    path("<int:label_id>/delete/", LabelDelete.as_view(), name="label_delete"),
]
