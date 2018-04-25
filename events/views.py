from django.views import generic

from .models import Events
from .models import Event_Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class EventView(generic.DetailView):
    model = Events
    template_name = 'events/events.html'



def view_events(request):
    total = {}
    events = Events.objects.filter().order_by('-event_date')
    print(events)
    #print(images)
    eve_images = []
    for event in events:

        images = Event_Image.objects.filter(event=event.id)
        event_images = {
            'event': event,
            'image': images
        }
        eve_images.append(event_images)
        print(images)
    template = 'events/events.html'
    context = {'events': eve_images}
    return render(request, template, context)