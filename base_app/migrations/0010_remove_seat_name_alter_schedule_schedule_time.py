# Generated by Django 4.0.6 on 2022-07-29 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0009_seat_name_alter_schedule_schedule_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='name',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 29, 9, 41, 43, 361176)),
        ),
    ]