# Generated by Django 5.1.5 on 2025-02-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bingo", "0017_alter_user_visibility"),
    ]

    operations = [
        migrations.AddField(
            model_name="tileinteraction",
            name="description",
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
