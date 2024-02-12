from django.db import models
from ..users.models import CustomUser
from ..statuses.models import Status
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_tasks')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='performed_tasks')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

