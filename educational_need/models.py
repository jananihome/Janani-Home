from djmoney.models.fields import MoneyField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class EducationalNeed(models.Model):
    user = models.ForeignKey('auth.User')
    permanent_address = models.TextField()
    additional_mobile_number = PhoneNumberField(blank=True)
    hide_mobile_number = models.BooleanField(default=False)
    additional_phone_number = models.CharField(max_length=20,blank=True,null=True)
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
    requirement_description = models.TextField()
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
        return 'Educational Need ' + str(self.pk)
