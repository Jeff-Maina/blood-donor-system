# Generated by Django 5.1.2 on 2024-11-13 07:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0002_alter_facilityprofile_open_days"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facilityprofile",
            name="is_approved",
            field=models.BooleanField(default=True),
        ),
    ]
