from django.contrib import admin

from .models import Events
from .models import Event_Image

admin.site.register(Events)
admin.site.register(Event_Image)