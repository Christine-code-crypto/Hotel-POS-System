# Generated by Django 4.2.4 on 2024-09-04 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("HotelApp", "0009_delete_room_remove_add_room_room_facility_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="authorregis",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
