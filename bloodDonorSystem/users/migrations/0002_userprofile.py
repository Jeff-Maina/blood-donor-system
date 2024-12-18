# Generated by Django 4.2.16 on 2024-11-06 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                ("date_of_birth", models.DateField()),
                ("phone", models.CharField(max_length=15)),
                ("county", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("blood_group", models.CharField(max_length=3)),
                ("gender", models.CharField(max_length=50)),
                ("weight", models.FloatField()),
                ("hemoglobin_level", models.FloatField()),
                ("is_in_good_health", models.BooleanField(default=True)),
                (
                    "emergency_contact_name",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "emergency_contact_phone",
                    models.CharField(blank=True, max_length=15),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
