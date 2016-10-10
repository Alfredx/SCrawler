# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20161008_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicitem',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 9, 7, 42, 21, 142136, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basicitem',
            name='write_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 9, 7, 42, 29, 96604, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stash',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 9, 7, 42, 54, 904351, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stash',
            name='write_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 9, 7, 42, 58, 213800, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stash',
            name='accountName',
            field=models.CharField(default=b'', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='stash',
            name='stash',
            field=models.CharField(default=b'', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='stash',
            name='stashType',
            field=models.CharField(default=b'', max_length=128, null=True),
        ),
    ]
