# Generated by Django 5.1.2 on 2024-11-13 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0002_alter_facilityprofile_open_days"),
        ("users", "0014_request"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="donations",
                to="facilities.facilityprofile",
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="donations",
                to="users.userprofile",
            ),
        ),
    ]
