from .models import Task
from django.forms import ModelForm
from django.utils.translation import gettext as _


class TaskCreateForm(ModelForm):

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
