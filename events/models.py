from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from easy_thumbnails.fields import ThumbnailerImageField


class Event(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name= 'Title',
        help_text= 'Event title visible in the browser and in search engine results.'
    )

    event_date = models.DateField('event date', default=timezone.now)

    description = models.TextField(
        max_length=200,
        verbose_name= 'Short description',
        help_text='Short description of the event.'
    )

    noindex = models.BooleanField(
        default=False,
        verbose_name='Don\'t index this page',
        help_text='Enable to tell search engine robots to not index this event page.',
    )

    sorting_value = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    name = models.CharField(max_length=255)
    image = ThumbnailerImageField(upload_to='event_images/')
    event = models.ForeignKey('Event', related_name="images", null=True, blank=True)
    sorting_value = models.IntegerField(default=0)

    def __str__(self):
        return self.name
