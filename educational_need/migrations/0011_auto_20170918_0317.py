# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-18 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational_need', '0010_auto_20170916_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalneed',
            name='hide_mobile_number',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='educationalneed',
            name='hide_permanent_address',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='educationalneed',
            name='hide_phone_number',
            field=models.BooleanField(default=True),
        ),
    ]
