# Generated by Django 4.0.6 on 2022-08-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0022_reservation_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='is_occupied',
            field=models.BooleanField(default=False),
        ),
    ]