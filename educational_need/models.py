import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from djmoney.models.fields import MoneyField
from ckeditor.fields import RichTextField


class EducationalNeed(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_uuid = models.CharField(max_length=18, blank=True, null=True)
    user = models.ForeignKey('auth.User')
    pub_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    permanent_address = models.TextField()
    additional_mobile_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )])
    hide_mobile_number = models.BooleanField(default=False)
    additional_phone_number = models.CharField(max_length=20,
                                               blank=True,
                                               null=True,
                                               validators=[
                                                   RegexValidator(
                                                       regex='^[0-9]*$',
                                                       message='Please use only numeric characters.'
                                                   )])
    hide_phone_number = models.BooleanField(default=False)
    current_address = models.TextField()
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

    def __str__(self):
        return 'Educational Need {}'.format(str(self.pk))

    def save(self, *args, **kwargs):
        if not self.date_uuid:
            self.date_uuid = self.pub_date.strftime('%Y/%m/%d/') + str(self.uuid)[:7]
        super().save(*args, **kwargs)
