# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-11 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
