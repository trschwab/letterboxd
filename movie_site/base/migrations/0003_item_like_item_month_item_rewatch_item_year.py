# Generated by Django 4.0.3 on 2023-11-27 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_item_day_item_film_item_rating_item_released'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='like',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='month',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='rewatch',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='year',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]