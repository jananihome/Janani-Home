import moneyed
from djmoney.models.fields import MoneyField
from django.db import models


class EducationalNeed(models.Model):
    user = models.ForeignKey('auth.User')
    permanent_address = models.TextField()
    current_address = models.TextField()
    college_school_address = models.TextField(blank=True, null=True)
    college_school_contact_details = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    status = models.CharField(max_length=200)
    amount_required = MoneyField(max_digits=10, decimal_places=2, default_currency='INR')
    requirement_description = models.TextField()

    # Define choices for communication_mode field
    # See: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.Field.choices
    PHONE = 'PH'
    MOBILE = 'MO'
    EMAIL = 'EM'
    COMMUNICATION_MODE_CHOICES = (
        (PHONE, 'Phone'),
        (MOBILE, 'Mobile'),
        (EMAIL, 'E-mail'),
    )
    # Define communication_mode field using choices defined above
    communication_mode = models.CharField(
        max_length=2,
        choices=COMMUNICATION_MODE_CHOICES,
        default=PHONE,
    )

    def __str__(self):
        """Return a friendly representation of an object, eg. in Django admin.
        See: https://docs.djangoproject.com/en/1.11/ref/models/instances/#str
        """
        return 'Educational Need ' + str(self.pk)
