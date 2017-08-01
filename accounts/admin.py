from django.contrib import admin
from .models import Profile, Country, State


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'country',
        'state',
        'city',
        'active_educational_need',
    )
admin.site.register(Profile, ProfileAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'country',
    )
admin.site.register(State, StateAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
    )
admin.site.register(Country, CountryAdmin)