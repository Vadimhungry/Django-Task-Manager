from django.contrib.auth.forms import (
    AuthenticationForm,
)
from .users.models import CustomUser
from django.utils.translation import gettext as _


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = \
            _("Username")
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = _("Password")

    class Meta:
        model = CustomUser
        fields = ("username", "password")
