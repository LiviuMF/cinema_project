# Generated by Django 4.0.6 on 2022-08-11 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0021_alter_schedule_schedule_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]