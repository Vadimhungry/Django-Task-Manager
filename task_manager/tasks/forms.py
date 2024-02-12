from .models import Task
from django import forms
from django.forms import ModelForm


class TaskCreateForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = "Имя"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["placeholder"] = "Описание"
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["executor"].widget.attrs["class"] = "form-select"
        self.user = user

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', ]
