# Generated by Django 5.1.3 on 2024-12-09 05:54

import django.db.models.deletion
from django.db import migrations, models
from django.db.migrations import RunPython


def populate_initial_data(apps, schema_editor):
    # Get the model classes (using apps.get_model() to ensure compatibility across migrations)
    List = apps.get_model("webapp", "List")
    List.objects.create(name="chores")
    List.objects.create(name="groceries")

    User = apps.get_model("webapp", "User")
    User.objects.create(name="Ivan")
    User.objects.create(name="Megan")
    User.objects.create(name="Isabela")
    User.objects.create(name="Luca")


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="List",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Meal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "day_of_week",
                    models.IntegerField(
                        choices=[
                            (0, "Monday"),
                            (1, "Tuesday"),
                            (2, "Wednesday"),
                            (3, "Thursday"),
                            (4, "Friday"),
                            (5, "Saturday"),
                            (6, "Sunday"),
                        ]
                    ),
                ),
                ("breakfast", models.CharField(blank=True, default="", max_length=100)),
                ("lunch", models.CharField(blank=True, default="", max_length=100)),
                ("dinner", models.CharField(blank=True, default="", max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("completed", models.BooleanField(default=False)),
                ("recurring", models.BooleanField(default=False)),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="webapp.list",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        related_query_name="item",
                        to="webapp.user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        RunPython(populate_initial_data),
    ]
