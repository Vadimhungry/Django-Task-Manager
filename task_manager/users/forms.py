from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username",
                  "password1", "password2"]


class CustomUserChangeForm(CustomUserCreationForm):
    def clean_username(self):
        return self.cleaned_data.get("username")
