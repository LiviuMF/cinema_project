# Generated by Django 4.0.6 on 2022-07-22 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_remove_movie_poster_movie_poster_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.DateTimeField(default='2022-07-22 18-09'),
        ),
    ]
