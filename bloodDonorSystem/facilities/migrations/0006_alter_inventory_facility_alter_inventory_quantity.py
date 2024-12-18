# Generated by Django 5.1.2 on 2024-11-14 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0005_alter_inventory_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="facility",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inventory",
                to="facilities.facilityprofile",
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="quantity",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
