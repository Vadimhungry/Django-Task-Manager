# Generated by Django 5.0.1 on 2024-02-12 09:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="performer",
            new_name="executor",
        ),
    ]
