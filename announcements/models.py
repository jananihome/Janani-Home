from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from easy_thumbnails.fields import ThumbnailerImageField
from smart_selects.db_fields import ChainedForeignKey

from accounts.models import Country, State


class Announcement(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name= 'Title',
        help_text= 'Announcement title visible in the browser and in search engine results.'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name= 'URL Slug',
        help_text='The slug will be used as URL of the page. Must be unique!'
    )
    published = models.BooleanField(
        default=True,
        help_text='Publish announcement on the list view.'
    )
    pub_date = models.DateTimeField('date published', default=timezone.now)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    state = ChainedForeignKey(
        State,
        on_delete=models.SET_NULL,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True
    )
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, blank=True)
    street_address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    description = models.CharField(
        max_length=200,
        verbose_name= 'Short description',
        help_text='Short description of the announcement to be displayed on the list view.'
    )
    content = RichTextField(
        config_name='admin',
        verbose_name= 'Content',
        help_text='Main announcement content displayed on the detail view in rich text (can contain images etc...).',
        blank=True,
        null=True
    )
    image = ThumbnailerImageField(
        upload_to='announcement_images',
        blank=True,
        null=True,
        verbose_name='Main image to be displayed on the list view.')
    closed = models.BooleanField(default=False)
    closed_date = models.DateTimeField('date closed', null=True, blank=True)
    closed_reason = models.TextField(null=True, blank=True)
    noindex = models.BooleanField(
        default=False,
        verbose_name='Don\'t index this page',
        help_text='Enable to tell search engine robots to not index this page.',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={'slug':self.slug})
    
    def get_status(self):
        if self.closed:
            return 'closed'
        return 'open'
