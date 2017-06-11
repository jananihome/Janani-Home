from django.shortcuts import render
# Model imports
from .models import EducationalNeed


def list_view(request):
    """Returns a view with a list of all EducationalNeed objects."""
    educational_needs = EducationalNeed.objects.all()
    template = 'educational_need/list_view.html'
    # Create context dictionary which can be accessed in template
    context = {'educational_needs': educational_needs}
    return render(request, template, context)
