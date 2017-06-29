from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
# Model imports
from .models import EducationalNeed
from accounts.models import Profile
# Form imports
from .forms import EducationalNeedForm, UserContactForm


def list_view(request):
    """Returns a listing with only active EducationalNeed objects."""
    # Select user profiles with an active educational need
    users = Profile.objects.filter(active_educational_need__isnull=False)
    # Select active educational needs from the above user set
    educational_needs = [user.active_educational_need for user in users]
    # Create context dictionary which can be accessed in template
    context = {'educational_needs': educational_needs,}
    template = 'educational_need/list_view.html'
    return render(request, template, context)


def detail_view(request, pk):
    """Returns a detailed view of a specific EducationalNeed object."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)

    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            toemail = educational_need.user.email
            fromemail = request.user.email

            email = EmailMessage(
                "Message from {} on Janani Care.".format(educational_need.user),
                message,
                "{} on Janani Care.".format(educational_need.user),
                [toemail],
                headers={'Reply-To': fromemail}
            )
            email.send()
            return redirect('message_sent')
    else:
        # Increment view count every time view is requested other than POST.
        # TODO: Find a way to increment view count only once per user session.
        educational_need.view_count += 1
        educational_need.save()

    # Load form class
    form = UserContactForm

    # Create context dictionary which can be accessed in template
    context = {'educational_need': educational_need, 'form': form}
    template = 'educational_need/detail_view.html'
    return render(request, template, context)

def message_sent(request):
    template = 'educational_need/message_sent.html'
    return render(request, template)

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
    
    # Check if user profile has required information for adding a need
	# It will be False if any of the fields is blank or null
    profile_complete = all([request.user.first_name, request.user.last_name,
                           request.user.email, request.user.profile.birth_date,
                           request.user.profile.mobile_number, request.user.profile.city,
                           request.user.profile.state, request.user.profile.country])
    
    # Create context dictionary which can be accessed in template
    context = {'form': form, 'profile complete': profile_complete}
    template = 'educational_need/form_view.html'
    return render(request, template, context)
