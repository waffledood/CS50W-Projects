# Generated by Django 3.1 on 2020-10-16 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auto_20201016_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='listing',
            new_name='listing_id',
        ),
    ]