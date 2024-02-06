from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Пароль"
        self.fields["password2"].widget.attrs["placeholder"] = "Подтверждение пароля"

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("first_name", "last_name", "username", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Фамилия"}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя пользователя"}
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Имя пользователя"
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = "Пароль"

    class Meta:
        model = CustomUser
        fields = ("username", "password")
