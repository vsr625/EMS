# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 09:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0013_auto_20171021_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 21, 9, 50, 40, 705660, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='participant',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('fd38f36d-1fb4-40ee-9970-9a2ee1a1364e'), primary_key=True, serialize=False),
        ),
    ]
