# Generated by Django 4.2.16 on 2024-11-10 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_customuser_facility_name_customuser_is_approved_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DonationEligibity",
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
                ("last_donation_date", models.DateField(blank=True, null=True)),
                ("weight", models.IntegerField(default=False)),
                ("pregnancy_status", models.CharField(max_length=50)),
                ("recent_illness", models.BooleanField(default=False)),
                ("recent_travel", models.BooleanField(default=False)),
                ("on_medication", models.BooleanField(default=False)),
                ("is_in_good_health", models.BooleanField(default=False)),
                ("is_breastfeeding", models.BooleanField(default=False)),
                ("chronic_condition", models.BooleanField(default=False)),
                ("eligible", models.BooleanField()),
                ("remarks", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
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
