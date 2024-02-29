from .models import Label
from django.forms import ModelForm


class LabelCreateForm(ModelForm):

    class Meta:
        model = Label
        fields = [
            "name",
        ]
