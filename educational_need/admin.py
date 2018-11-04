from django.contrib import admin

from .models import EducationalNeed


class EducationalNeedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_country',
        'get_state',
        'get_city',
        'amount_required',
        'closed',
        'pub_date'
    )

    def get_country(self, obj):
        return obj.user.profile.country
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'user__profile__country'

    def get_state(self, obj):
        return obj.user.profile.state
    get_state.short_description = 'State'
    get_state.admin_order_field = 'user__profile__state'

    def get_city(self, obj):
        return obj.user.profile.city
    get_city.short_description = 'City'
    get_city.admin_order_field = 'user__profile__city'


admin.site.register(EducationalNeed, EducationalNeedAdmin)