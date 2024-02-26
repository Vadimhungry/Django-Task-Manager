import django_filters
from django import forms
from .models import Task
from ..statuses.models import Status
from ..users.models import CustomUser
from ..labels.models import Label


class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Метки",
    )
    self_tasks = django_filters.BooleanFilter(
        field_name="author",
        method="filter_created_by_current_user",
        label="Только свои задачи",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]

    def filter_created_by_current_user(self, queryset, author, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
