from django.views import generic

from .models import Event
from .models import EventImage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/events.html'



def view_events(request):
    total = {}
    events = Event.objects.filter().order_by('-event_date')
    print(events)
    #print(images)
    eve_images = []
    for event in events:

        images = EventImage.objects.filter(event=event.id)
        event_images = {
            'event': event,
            'image': images
        }
        eve_images.append(event_images)
        print(images)
    template = 'events/events.html'
    context = {'events': eve_images}
    return render(request, template, context)
