from .models import Task
from django.forms import ModelForm


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
