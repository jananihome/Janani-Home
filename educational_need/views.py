from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# Model imports
from .models import EducationalNeed
from accounts.models import Profile
# Form imports
from .forms import EducationalNeedForm, UserContactForm


class EducationalNeedListView(ListView):
    """Returns a listing with only active EducationalNeed objects."""

    model = EducationalNeed
    template_name = 'educational_need/list_view.html'
    paginate_by = 1


    def get_queryset(self):
        # Select user profiles with an active educational need
        users = Profile.objects.filter(active_educational_need__isnull=False)
        # Select active educational needs from the user list
        queryset = [user.active_educational_need for user in users]
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'JananiCare - find and help people in educational need'
        users = Profile.objects.filter(active_educational_need__isnull=False)
        educational_needs = [user.active_educational_need for user in users]
        data['countries'] = [need.user.profile.country.name for need in educational_needs]
        return data


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


@login_required
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
            return redirect('view_profile')
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
    context = {'form': form, 'profile_complete': profile_complete}
    template = 'educational_need/form_view.html'
    return render(request, template, context)


@login_required
def edit_educational_need(request, pk):
    """Returns a view for editing EducationalNeed objects and handles POST
    requests submitted through the form."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
	
    # If request method is POST, process form data.
    if request.method == 'POST':
        # Collect data from the form.
        form = EducationalNeedForm(request.POST, request.FILES, instance=educational_need)
        # If form data is valid, process data and save.
        if form.is_valid():
            form.save()
            # Redirect after submitting the form
            return redirect('view_profile')
    # If request is not POST, create empty form.
    else:
        form = EducationalNeedForm(instance=educational_need)
    
    # Check if user profile has required information for adding a need
	# It will be False if any of the fields is blank or null
    profile_complete = all([request.user.first_name, request.user.last_name,
                           request.user.email, request.user.profile.birth_date,
                           request.user.profile.mobile_number, request.user.profile.city,
                           request.user.profile.state, request.user.profile.country])
    
    # Create context dictionary which can be accessed in template
    context = {'form': form, 'profile_complete': profile_complete}
    template = 'educational_need/form_view.html'
    return render(request, template, context)


@login_required
def delete_need(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    educational_need.delete()
    return redirect('view_profile')


@login_required
def activate_need(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    user_profile = request.user.profile
    user_profile.active_educational_need = educational_need
    user_profile.save()
    return redirect('view_profile')
