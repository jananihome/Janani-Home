from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import EducationalNeed


def list_view(request):

    educational_needs = EducationalNeed.objects.all()
    template = 'educational_need/list_view.html'
    context = {'educational_needs': educational_needs}

    return render(request, template, context)
