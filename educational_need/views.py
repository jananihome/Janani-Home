from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView

from accounts.models import Profile, Country, State
from comment.models import Comment
from .models import EducationalNeed
from .forms import EducationalNeedForm, UserContactForm


class EducationalNeedListView(ListView):
    """Returns a listing with only active EducationalNeed objects."""

    model = EducationalNeed
    template_name = 'educational_need/list_view.html'
    paginate_by = 6
    state_=None
    country_=None
    query_=None

    def get_queryset(self):

        # Select user profiles with an active educational need
        users = Profile.objects.filter(active_educational_need__isnull=False).select_related('active_educational_need').select_related('user').order_by('-active_educational_need__pk')

        # Maybe in future we use this variable
        # filer_done = False

        # Country filter
        if self.request.GET.get('country'):
            try:
                country = Country.objects.get(pk=self.request.GET.get('country'))
                users = users.filter(country = country)
                # may be in future we use this variable
                # filer_done = True
                self.country_ = country
            except Exception as e:
                pass

        # State filter
        if self.request.GET.get('state'):
            try:
                state = State.objects.get(pk=self.request.GET.get('state'))
                users = users.filter(state = state)
                # filer_done = True
                self.state_=state
            except Exception as e:
                pass

        # Commented out below lines, because they were hiding needs of other
        # users from the list view when user was authenticated.
        #if (not filer_done) and self.request.user.is_authenticated():
        #    try:
        #        country = Profile.objects.get(user=self.request.user).country
        #        users = users.filter(country = country)
        #        state = Profile.objects.get(user=self.request.user).state
        #        users = users.filter(state = state)
        #    except Exception as e:
        #        pass

        if self.request.GET.get('query'):
            query = self.request.GET.get('query')
            users=users.filter(Q(city__icontains=query)|Q(district__icontains=query)|Q(zip_code__icontains=query)|Q(mobile_number__icontains=query)|Q(phone_number__icontains=query)| Q(about__icontains=query))
            self.query_=self.request.GET.get('query')

        # Select active educational needs from the user list
        queryset = [user.active_educational_need for user in users]
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Country list
        data['countries'] = Country.objects.values('name','code','pk')
        data['comments'] = Comment.objects.filter(published=True).order_by('-pk')[:3]
        if self.country_:
            data['country_'] = self.country_.pk
            data['active_country'] = self.country_.name
            data['states'] = State.objects.filter(country=self.country_).values('name','code','pk')
        if self.state_:
            data['state_'] = self.state_.pk
            data['active_state'] = self.state_.name
        if self.query_:
            data['query_'] = self.query_
            data['active_query'] = self.query_

        return data


def detail_view(request, pk):
    """Returns a detailed view of a specific EducationalNeed object."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)

    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():
            subject = 'Message from {} on Janani Care.'.format(request.user)
            message = form.cleaned_data['message']
            from_name = '{} on Janani Care.'.format(request.user)
            to_email = educational_need.user.email
            from_email = request.user.email
            headers = {'Reply-To': from_email}
            email = EmailMessage(subject, message, from_name, [to_email], headers=headers)
            email.send()
            messages.success(request, 'Message sent.')
    else:
        # On non-POST requests, increment view_count once per user session
        try:
            request.session['viewed_need_{}'.format(educational_need.pk)]
        except KeyError:
            request.session['viewed_need_{}'.format(educational_need.pk)] = True
            educational_need.view_count += 1
            educational_need.save()

    form = UserContactForm
    context = {'educational_need': educational_need, 'form': form}
    template = 'educational_need/detail_view.html'
    return render(request, template, context)


@login_required
@transaction.atomic
def add_need(request):
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
            # Activate the need if no other need is active
            if not eductional_need.user.profile.active_educational_need:
                eductional_need.user.profile.active_educational_need = eductional_need
                eductional_need.user.profile.save()
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
def edit_need(request, pk):
    """Returns a view for editing EducationalNeed objects and handles POST
    requests submitted through the form."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if educational_need.closed:
        raise Http404("This need has been closed!")
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
    if educational_need.closed:
        raise Http404('This need has been closed!')
    educational_need.delete()
    return redirect('view_profile')


@login_required
def activate_need(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if educational_need.closed:
        raise Http404('This need has been closed!')
    user_profile = request.user.profile
    user_profile.active_educational_need = educational_need
    user_profile.save()
    return redirect('view_profile')


@login_required
def deactivate_need(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if educational_need.closed:
        raise Http404('This need has been closed!')
    user_profile = request.user.profile
    user_profile.active_educational_need = None
    user_profile.save()
    return redirect('view_profile')
