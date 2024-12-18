# Generated by Django 5.1.2 on 2024-11-12 20:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0013_alter_donation_donation_type_alter_donation_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Request",
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
                ("request_type", models.CharField(max_length=50)),
                ("request_date", models.DateField()),
                ("needed_by", models.DateTimeField()),
                ("request_amount", models.DecimalField(decimal_places=2, max_digits=5)),
                ("status", models.CharField(max_length=50)),
                ("rejection_reason", models.TextField(blank=True, null=True)),
                (
                    "urgency_level",
                    models.CharField(
                        choices=[
                            ("normal", "normal"),
                            ("urgent", "urgent"),
                            ("critical", "critical"),
                        ],
                        max_length=50,
                    ),
                ),
                ("remarks", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
