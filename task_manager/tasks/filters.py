import django_filters
from django import forms
from .models import Task
from ..statuses.models import Status
from ..users.models import CustomUser
from ..labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-select is-valid"}),
        label="Статус",
    )
    executor = django_filters.ModelChoiceFilter(
        field_name="executor",
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={"class": "form-select is-valid"}),
        label="Исполнитель",
    )
    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={"class": "form-select is-valid"}),
        label="Метки",
    )
    self_tasks = django_filters.BooleanFilter(
        field_name="author",
        method="filter_created_by_current_user",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input is-valid"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]

    def filter_created_by_current_user(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
