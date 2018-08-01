# Generated by Django 2.0.5 on 2018-07-21 19:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/default.jpg', null=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 21, 19, 44, 51, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
