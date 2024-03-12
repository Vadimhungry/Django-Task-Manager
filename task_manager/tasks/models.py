from django.db import models
from ..users.models import CustomUser
from ..statuses.models import Status
from ..labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        blank=True,
        verbose_name=_("Executor"),
        null=True,
    )
    author = models.ForeignKey(
        get_user_model(),
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
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_("Labels")
    )

    def __str__(self):
        return self.name
