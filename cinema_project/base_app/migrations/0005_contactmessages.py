# Generated by Django 4.0.6 on 2022-07-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_hall_movie_hall'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(default=None, max_length=100)),
                ('phone', models.CharField(default=None, max_length=20)),
                ('cinema', models.CharField(default=None, max_length=50)),
                ('subject', models.CharField(default=None, max_length=30)),
                ('message', models.TextField(default=None)),
            ],
        ),
    ]