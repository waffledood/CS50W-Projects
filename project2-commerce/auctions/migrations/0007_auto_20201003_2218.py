# Generated by Django 3.1 on 2020-10-03 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_auction_aa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='descripion',
            new_name='description',
        ),
    ]