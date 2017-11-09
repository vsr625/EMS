# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 09:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0022_auto_20171109_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('041fa9d0-39bc-4c58-8ef9-1f647849d11f'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='RegNo',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Register Number is Invalid', regex='^1RV\\d{2}[a-zA-Z]{2}\\d{3}$')]),
        ),
    ]