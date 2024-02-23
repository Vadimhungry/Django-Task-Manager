from .models import Task
from django.forms import ModelForm
from django.utils.translation import gettext as _


class TaskCreateForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = _("Name")
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = _("Имя")
        self.fields["description"].label = _("Description")
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["placeholder"] = _("Описание")
        self.fields["status"].label = _("Status")
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["executor"].label = _("Executor")
        self.fields["executor"].widget.attrs["class"] = "form-select"
        self.fields["labels"].label = _("Labels")
        self.fields["labels"].widget.attrs["class"] = "form-select"
        self.user = user


    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
