from django import forms
from .models import Status


class StatusCreateForm(forms.ModelForm):
    name = forms.CharField(label="Имя")

    def __init__(self, *args, **kwargs):
        super(StatusCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = "Имя"

    class Meta:
        model = Status
        fields = ["name"]
