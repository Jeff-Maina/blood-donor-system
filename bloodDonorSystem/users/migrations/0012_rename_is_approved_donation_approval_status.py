# Generated by Django 5.1.2 on 2024-11-11 13:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_donation_is_approved"),
    ]

    operations = [
        migrations.RenameField(
            model_name="donation",
            old_name="is_approved",
            new_name="approval_status",
        ),
    ]
