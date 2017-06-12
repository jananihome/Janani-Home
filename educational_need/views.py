from django.shortcuts import get_object_or_404, redirect, render
# Model imports
from .models import EducationalNeed
# Form imports
from .forms import EducationalNeedForm


def list_view(request):
    """Returns a view with a list of all EducationalNeed objects."""
    educational_needs = EducationalNeed.objects.all()
    
    # Create context dictionary which can be accessed in template
    context = {'educational_needs': educational_needs}
    template = 'educational_need/list_view.html'
    return render(request, template, context)


def detail_view(request, pk):
    """Returns a detailed view of a specific EducationalNeed object."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    
    # Create context dictionary which can be accessed in template
    context = {'educational_need': educational_need}
    template = 'educational_need/detail_view.html'
    return render(request, template, context)


def add_educational_need(request):
    """Returns a view for adding EducationalNeed objects and handles POST
    requests submitted through the form."""
    
    # If request method is POST, process form data.
    if request.method == 'POST':
        # Collect data from the form.
        form = EducationalNeedForm(request.POST, request.FILES)
        # If form data is valid, process data and save.
        if form.is_valid():
            # False save to variable first, because we need to modify data
            # before commiting it to db.
            eductional_need = form.save(commit=False)
            # Set user to currently logged in user.
            eductional_need.user = request.user
            # Save model data in db.
            eductional_need.save()
            # Redirect after submitting the form
            return redirect('list_view')
    # If request is not POST, create empty form.
    else:
        form = EducationalNeedForm()
        
    # Create context dictionary which can be accessed in template
    context = {'form': form}
    template = 'educational_need/form_view.html'
    return render(request, template, context)
