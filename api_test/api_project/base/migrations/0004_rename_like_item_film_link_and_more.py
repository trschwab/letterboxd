# Generated by Django 4.0.3 on 2023-11-27 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_item_like_item_month_item_rewatch_item_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='like',
            new_name='film_link',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='rewatch',
            new_name='review_link',
        ),
    ]
