# Generated by Django 4.2.4 on 2024-09-05 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("HotelApp", "0016_alter_online_booking_check_in_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="online_booking",
            name="Nid_No",
        ),
    ]
