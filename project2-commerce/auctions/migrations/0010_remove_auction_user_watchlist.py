# Generated by Django 3.1 on 2020-10-05 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_user_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='user_watchlist',
        ),
    ]