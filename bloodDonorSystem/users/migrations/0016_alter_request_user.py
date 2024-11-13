# Generated by Django 5.1.2 on 2024-11-13 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0015_donation_facility_alter_donation_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.userprofile"
            ),
        ),
    ]