# Generated by Django 5.1.2 on 2024-11-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_request_facility"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="request",
            name="request_date",
        ),
        migrations.AlterField(
            model_name="request",
            name="request_type",
            field=models.CharField(
                choices=[
                    ("whole blood", "Whole Blood Donation"),
                    ("plasma", "Plasma Donation"),
                    ("platelets", "Platelet Donation"),
                    ("double red cells", "Double Red Cell Donation"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="request",
            name="status",
            field=models.CharField(default="pending", max_length=50),
        ),
    ]
