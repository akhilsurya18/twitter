# Generated by Django 2.0.5 on 2018-07-27 15:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0004_auto_20180727_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 27, 15, 35, 54, tzinfo=utc)),
        ),
    ]
