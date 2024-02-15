from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_delete


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def can_be_deleted(self):
        return not self.task_set.exists()


@receiver(pre_delete, sender=Label)
def prevent_label_deletion(sender, instance, **kwargs):
    if instance.can_be_deleted():
        return
    else:
        # Отменяем удаление метки
        raise ValueError("Cannot delete label because it is associated with tasks.")