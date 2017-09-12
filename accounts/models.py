from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
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
    code = models.CharField(max_length=2)
    country = models.ForeignKey('Country', null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Define model for user profile with one-to-one relationship with User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
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
    image =  ThumbnailerImageField(upload_to='profile_images', blank=True,
                                   null=True)

    def get_full_name(self):
        if self.middle_name:
            return '{} {} {}'.format(self.user.first_name, self.middle_name, self.user.last_name)
        else:
            return '{} {}'.format(self.user.first_name, self.user.last_name)

    def __str__(self):
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
