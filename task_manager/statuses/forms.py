from django import forms
from .models import Status


class StatusCreateForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
