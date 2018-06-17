from django.contrib.auth.models import User

from accounts.models import Profile, Country, State
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        exclude = ()


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        exclude = ()


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        exclude = ()
