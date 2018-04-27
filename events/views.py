from django.shortcuts import render
from django.views import generic

from .models import Event
from .models import EventImage


def events(request):
    events = Event.objects.filter().order_by('-event_date')
    template = 'events/events.html'
    context = {'events': events}

    return render(request, template, context)
