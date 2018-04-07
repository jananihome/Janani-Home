# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-06 22:54
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0019_auto_20180403_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Announcement title visible in the browser and in search engine results.', max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(help_text='The slug will be used as URL of the page. Must be unique!', max_length=200, unique=True, verbose_name='URL Slug')),
                ('published', models.BooleanField(default=True, help_text='Publish announcement on the list view.')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('street_address', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=200)),
                ('description', models.CharField(help_text='Short description of the announcement.', max_length=200, verbose_name='Short description')),
                ('content', ckeditor.fields.RichTextField(blank=True, help_text='Main announcement content displayed in rich text (can contain images etc...).', null=True, verbose_name='Content')),
                ('closed', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(blank=True, null=True, verbose_name='date closed')),
                ('closed_reason', models.TextField(blank=True, null=True)),
                ('noindex', models.BooleanField(default=False, help_text='Enable to tell search engine robots to not index this page.', verbose_name="Don't index this page")),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Country')),
                ('state', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.State')),
            ],
        ),
    ]