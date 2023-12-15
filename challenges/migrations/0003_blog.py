# Generated by Django 4.2.3 on 2023-12-15 16:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("challenges", "0002_laptop"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
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
                ("title", models.CharField(max_length=256)),
                ("text", models.TextField()),
                ("author", models.CharField(max_length=256)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "published"),
                            ("not published", "not published"),
                            ("banned", "banned"),
                        ],
                        max_length=25,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("published_at", models.DateTimeField(null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Sience fiction", "Sience fiction"),
                            ("Drama", "Drama"),
                            ("Comedia", "Comedia"),
                            ("Sience", "Sience"),
                            ("Detective", "Detective"),
                            ("Medicine", "Medicine"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
            },
        ),
    ]
