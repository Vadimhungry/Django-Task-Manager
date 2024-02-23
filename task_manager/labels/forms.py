from .models import Label
from django.forms import ModelForm


class LabelCreateForm(ModelForm):
    # def __init__(self, user=None, *args, **kwargs):
    #     super(LabelCreateForm, self).__init__(*args, **kwargs)
    #     self.fields["name"].widget.attrs["class"] = "form-control"
    #     self.fields["name"].widget.attrs["placeholder"] = "Имя"

    class Meta:
        model = Label
        fields = [
            "name",
        ]
