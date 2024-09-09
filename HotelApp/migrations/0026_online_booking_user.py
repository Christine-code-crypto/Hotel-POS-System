# Generated by Django 4.2.4 on 2024-09-08 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("HotelApp", "0025_invoice_mpesa_status_invoice_mpesa_transaction_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="online_booking",
            name="user",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]