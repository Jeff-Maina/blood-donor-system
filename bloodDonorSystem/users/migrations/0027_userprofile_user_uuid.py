# Generated by Django 5.1.2 on 2024-11-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0026_donation_donation_id_request_request_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="user_uuid",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
