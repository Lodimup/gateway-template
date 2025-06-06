# Generated by Django 5.2 on 2025-05-11 15:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appaccount", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="realtime_exchange",
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(
                choices=[
                    ("m", "Male"),
                    ("f", "Female"),
                    ("n", "Non-binary"),
                    ("o", "Other"),
                    ("u", "Unknown"),
                ],
                default=None,
                null=True,
            ),
        ),
    ]
