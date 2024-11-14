# Generated by Django 5.1.2 on 2024-11-14 23:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_rename_notifications_notification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="message",
        ),
        migrations.AddField(
            model_name="notification",
            name="type",
            field=models.CharField(default="", max_length=50, null=True),
        ),
    ]
