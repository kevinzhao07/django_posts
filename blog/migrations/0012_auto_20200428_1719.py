# Generated by Django 3.0.4 on 2020-04-28 21:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 17, 19, 33, 413057)),
        ),
        migrations.AlterField(
            model_name='like',
            name='date_liked',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 17, 19, 33, 413057)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 17, 19, 33, 414016)),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=560),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 17, 19, 33, 412058)),
        ),
    ]
