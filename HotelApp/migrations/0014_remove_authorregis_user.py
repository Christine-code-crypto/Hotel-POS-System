# Generated by Django 4.2.4 on 2024-09-04 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("HotelApp", "0013_authorregis_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="authorregis",
            name="user",
        ),
    ]
