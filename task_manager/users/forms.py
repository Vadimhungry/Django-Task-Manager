from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
        )



class CustomUserChangeForm(CustomUserCreationForm):
    def clean_username(self):
        return self.cleaned_data.get("username")
