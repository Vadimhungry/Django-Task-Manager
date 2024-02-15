from django.db import models
from ..users.models import CustomUser
from ..statuses.models import Status
from  ..labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    executor = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="authored_tasks"
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="performed_tasks"
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label)