# Generated by Django 3.1.2 on 2020-10-29 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subreddit_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='subreddit',
            table='subreddit_data',
        ),
    ]