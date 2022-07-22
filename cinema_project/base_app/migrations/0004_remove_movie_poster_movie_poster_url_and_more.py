# Generated by Django 4.0.6 on 2022-07-22 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_alter_movie_imdb_id_alter_schedule_schedule_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster',
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.CharField(default=None, max_length=400),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 22, 10, 29, 9, 754653)),
        ),
    ]
