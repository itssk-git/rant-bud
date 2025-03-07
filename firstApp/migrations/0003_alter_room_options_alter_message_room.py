# Generated by Django 5.1.4 on 2024-12-24 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("firstApp", "0002_topic_room_host_message_room_topic"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={"ordering": ["-updated", "-created"]},
        ),
        migrations.AlterField(
            model_name="message",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="firstApp.room",
            ),
        ),
    ]
