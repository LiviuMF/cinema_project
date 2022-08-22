# Generated by Django 4.0.6 on 2022-08-02 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0013_alter_schedule_schedule_time_alter_seat_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 12, 47, 22, 814841)),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('seat', 'schedule')},
        ),
    ]