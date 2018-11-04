import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from djmoney.models.fields import MoneyField
from ckeditor.fields import RichTextField
from smart_selects.db_fields import ChainedForeignKey
from easy_thumbnails.fields import ThumbnailerImageField


class EducationalNeed(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_uuid = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('auth.User')
    pub_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    permanent_address = models.TextField()
    hide_permanent_address = models.BooleanField(default=True)
    additional_mobile_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )])
    hide_mobile_number = models.BooleanField(default=True)
    additional_phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(regex='^[0-9]*$',
                                   message='Please use only numeric characters.')])
    hide_phone_number = models.BooleanField(default=True)
    current_address = models.TextField()
    hide_current_address = models.BooleanField(default=True)
    college_school_address = models.TextField()
    college_school_contact_details = models.CharField(max_length=200)
    view_count = models.IntegerField(default=0)
    amount_required = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='INR',
        blank=True,
        null=True
    )
    requirement_description = RichTextField()
    youtube_url = models.URLField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    # Define choices for communication_mode field
    PHONE = 'PH'
    MOBILE = 'MO'
    EMAIL = 'EM'
    COMMUNICATION_MODE_CHOICES = (
        (PHONE, 'Phone'),
        (MOBILE, 'Mobile'),
        (EMAIL, 'E-mail'),
    )

    communication_mode = models.CharField(
        max_length=2,
        choices=COMMUNICATION_MODE_CHOICES,
        default=PHONE,
    )

    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    extended = models.BooleanField(default=False)
    ext_first_name = models.CharField(max_length=200, blank=True, null=True)
    ext_middle_name = models.CharField(max_length=200, blank=True, null=True)
    ext_last_name = models.CharField(max_length=200, blank=True, null=True)
    # Gender field
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    ext_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE, blank=True, null=True)
    ext_birth_date = models.DateField(blank=True, null=True)
    ext_country = models.ForeignKey(
        'accounts.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ext_state = ChainedForeignKey(
        'accounts.State',
        on_delete=models.SET_NULL,
        chained_field="ext_country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True
    )
    ext_zip_code = models.CharField(max_length=10, blank=True)
    ext_city = models.CharField(max_length=50, blank=True)
    ext_district = models.CharField(max_length=50, blank=True)
    ext_about = RichTextField(null=True, blank=True)
    ext_image = ThumbnailerImageField(
        upload_to='profile_images',
        blank=True,
        null=True,
        verbose_name='Person\'s picture')
    ext_email = models.EmailField(blank=True, null=True)


    def __str__(self):
        return 'Educational Need {}'.format(str(self.pk))

    def get_absolute_url(self):
        return reverse('detail_view', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if not self.date_uuid:
            self.date_uuid = self.pub_date.strftime('%Y/%m/%d/') + str(self.uuid)
        super().save(*args, **kwargs)

    def create_youtube_embed_link(self):
        return str(self.youtube_url).replace('watch?v=', 'embed/')
