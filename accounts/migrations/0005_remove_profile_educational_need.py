# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_educational_need'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='educational_need',
        ),
    ]