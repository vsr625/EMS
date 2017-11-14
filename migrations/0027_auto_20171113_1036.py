# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EMS', '0026_auto_20171113_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='Venue',
            field=models.CharField(choices=[('s', 'New Sports Complex'), ('i', 'IEM Auditorium'), ('m', 'Mini Canteen'),
                                            ('c', 'CSE Department'), ('d', 'Mathematics Department')], default='s',
                                   max_length=15),
        ),
    ]