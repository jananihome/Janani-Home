from django.views import generic

from .models import Events
from .models import Event_Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class EventView(generic.DetailView):
    model = Events
    template_name = 'events/events.html'


@login_required
def view_events(request):

    events = Events.objects.filter()
    images = Event_Image.objects.filter()
    print(images)
    for image in images:
        print(image)
        print(image.document)
    template = 'events/events.html'
    context = {'events': events, 'images': images}
    return render(request, template, context)