# Generated by Django 4.0.6 on 2022-08-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0018_movie_poster_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster_image',
            field=models.ImageField(default='media/images/tt0012349.png', upload_to=''),
        ),
    ]