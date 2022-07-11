# Generated by Django 4.0.6 on 2022-07-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('poster', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('imdb', models.FloatField()),
                ('url', models.CharField(max_length=400)),
                ('duration', models.FloatField()),
            ],
        ),
    ]