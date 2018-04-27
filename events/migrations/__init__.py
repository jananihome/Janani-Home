from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Page title visible in the browser and in search engine results.', max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(help_text='The slug will be used as URL of the page. Must be unique!', max_length=200, unique=True, verbose_name='URL Slug')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('event_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('description', models.CharField(help_text='Short description of the page.', max_length=200, verbose_name='Short description')),
                ('content', ckeditor.fields.RichTextField(blank=True, help_text='Main page content displayed in rich text.', null=True, verbose_name='Content')),
                ('noindex', models.BooleanField(default=False, help_text='Enable to tell search engine robots to not index this page.', verbose_name="Don't index this page")),
                ('sorting_value', models.IntegerField(default=0)),
            ],
        ),
    ]
