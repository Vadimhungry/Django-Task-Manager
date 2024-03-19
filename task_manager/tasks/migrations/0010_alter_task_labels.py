# Generated by Django 5.0.2 on 2024-03-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labels", "0002_alter_label_name"),
        ("tasks", "0009_alter_task_executor_alter_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                blank=True, to="labels.label", verbose_name="Labels"
            ),
        ),
    ]