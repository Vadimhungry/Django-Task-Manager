from django.db import models
from ..users.models import CustomUser
from ..statuses.models import Status
from ..labels.models import Label
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Executor"),
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="performed_tasks",
        verbose_name=_("Author"),
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_("Status")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    labels = models.ManyToManyField(Label, verbose_name=_("Labels"))

    def __str__(self):
        return self.name