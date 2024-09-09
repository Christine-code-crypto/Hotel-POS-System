# Generated by Django 4.2.4 on 2024-09-07 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("HotelApp", "0021_invoice_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to="HotelApp.add_room",
            ),
        ),
    ]