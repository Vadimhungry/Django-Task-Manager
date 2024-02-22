from django import forms
from .models import Status
from django.utils.translation import gettext as _

class StatusCreateForm(forms.ModelForm):
    # name = forms.CharField(label=_("Name"))

    def __init__(self, *args, **kwargs):
        super(StatusCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = _("Name")

    class Meta:
        model = Status
        fields = ["name"]
