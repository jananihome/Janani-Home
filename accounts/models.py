from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from educational_need.models import EducationalNeed

class Profile(models.Model):
    """
    Define model for user profile with one-to-one relationship with User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = CountryField(blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(blank=True)
    about = models.TextField(max_length=500, blank=True)
    educational_need = models.OneToOneField(EducationalNeed,
                                            on_delete=models.SET_NULL,
                                            blank=True, null=True)

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
