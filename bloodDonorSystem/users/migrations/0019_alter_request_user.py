# Generated by Django 5.1.2 on 2024-11-13 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0018_remove_request_request_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="requests",
                to="users.userprofile",
            ),
        ),
    ]