from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from educational_need.models import EducationalNeed
from easy_thumbnails.fields import ThumbnailerImageField
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.fields import RichTextField


class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    country = models.ForeignKey('Country', null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Define model for user profile with one-to-one relationship with User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, null=True, blank=True)

    # Define choices for gender field
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE,
    )

    birth_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )])
    mobile_number_2 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )],
        verbose_name='Additional mobile number')
    hide_mobile_number = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )])
    phone_number_2 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )],
        verbose_name='Additional phone number')
    hide_phone_number = models.BooleanField(default=False)
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
    zip_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    about = RichTextField()
    active_educational_need = models.ForeignKey(
        EducationalNeed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = ThumbnailerImageField(
        upload_to='profile_images',
        blank=True,
        null=True,
        verbose_name='Profile image')
    unconfirmed_email = models.EmailField(blank=True, null=True)
    is_volunteer = models.BooleanField(
        default=False,
        verbose_name='I want to be a volunteer',
        help_text='Select this if you want to become a volunteer for Janani Care or other organization. You will receive email with instructions when we review your application.')
    organization_id = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name='Organization',
        help_text='Only for volunteers. Select the organization you want to work for as a volunteer.',
        on_delete=models.SET_NULL,
        limit_choices_to={'is_organization': True},)
    is_organization = models.BooleanField(default=False)
    organization_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='NGO/Organization name')
    fax_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Please use only numeric characters.'
            )])
    organization_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Address')
    additional_contact_details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def get_age(self):
        return timezone.now().year - self.birth_date.year

    def get_full_name(self):
        if self.middle_name:
            return '{} {} {}'.format(self.user.first_name, self.middle_name,
                                     self.user.last_name)
        else:
            return '{} {}'.format(self.user.first_name, self.user.last_name)

    def __str__(self):
        if self.organization_name:
            return self.organization_name
        else:
            return self.user.username


# Define signals to update user profile whenever we create/update User model.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create Profile object whenever new User object is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Update Profile object whenever new User object is updated.
    """
    instance.profile.save()
