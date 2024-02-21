from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )  # Fields to display in the list view
    search_fields = ["username"]
