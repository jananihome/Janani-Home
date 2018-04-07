from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone


class Events(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name= 'Title',
        help_text= 'Page title visible in the browser and in search engine results.'
    )

    event_date = models.DateTimeField('event date', default=timezone.now)
    description = models.CharField(
        max_length=200,
        verbose_name= 'Short description',
        help_text='Short description of the page.'
    )

    # content = RichTextField(
    #     config_name='admin',
    #     verbose_name= 'Content',
    #     help_text='Main page content displayed in rich text.',
    #     blank=True,
    #     null=True)
    #
    # noindex = models.BooleanField(
    #     default=False,
    #     verbose_name='Don\'t index this page',
    #     help_text='Enable to tell search engine robots to not index this page.',
    # )

    # show_in_menu = models.BooleanField(
    #     default=True,
    #     verbose_name='Show in navigation',
    #     help_text='Show page in website top navigation menu.',
    # )

    # page_icon = models.CharField(
    #     max_length=200,
    #     blank=True,
    #     null=True,
    #     verbose_name='Font Awesome icon class',
    #     help_text='Enter a Font Awesome class name for the icon in navigation, e.g. "fa fa-info". See all icons here: http://fontawesome.io/icons/',
    #
    # )

    sorting_value = models.IntegerField(default=0)

    def __str__(self):
        return self.title



class Event_Image(models.Model):
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    event = models.ForeignKey('Events', null=True)

