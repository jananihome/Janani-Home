# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-03 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_profile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_organization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_volunteer',
            field=models.BooleanField(default=False),
        ),
    ]
