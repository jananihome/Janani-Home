from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView

from accounts.models import Country, Profile, State
from comment.models import Comment
from .models import EducationalNeed
from .forms import EducationalNeedForm, EducationalNeedExtendedForm, UserContactForm


class EducationalNeedListView(ListView):
    """Returns a listing with only active EducationalNeed objects."""

    model = EducationalNeed
    template_name = 'educational_need/list_view.html'
    paginate_by = 4
    query_ = None

    def get_queryset(self):

        # Select active educational needs
        active_needs = EducationalNeed.objects.filter(is_active=True).order_by('-pk')

        # Search query
        if self.request.GET.get('query'):
            query = self.request.GET.get('query')
            active_needs = active_needs.filter(Q(user__profile__city__icontains=query)|Q(user__profile__district__icontains=query)|Q(user__profile__zip_code__icontains=query)|Q(user__profile__mobile_number__icontains=query)|Q(user__profile__phone_number__icontains=query)| Q(user__profile__about__icontains=query))
            self.query_ = self.request.GET.get('query')

        return active_needs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Country list
        data['countries'] = Country.objects.values('name','code','pk')
        data['comments'] = Comment.objects.filter(published=True).order_by('-pk')[:3]

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
            if educational_need.extended:
                to_email = educational_need.ext_email
            else:
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
    if request.user.profile.multiple_needs:
        extended = True
    else:
        extended = False

    # If request method is POST, process form data.
    if request.method == 'POST':
        if extended:
            form = EducationalNeedExtendedForm(request.POST, request.FILES)
        else:
            form = EducationalNeedForm(request.POST, request.FILES)
        # If form data is valid, process data and save.
        if form.is_valid():
            # False save to variable first, because we need to modify data
            # before committing it to db.
            educational_need = form.save(commit=False)
            # Set user to currently logged in user.
            educational_need.user = request.user
            if extended:
                educational_need.extended = True
                educational_need.is_active = True
            else:
                # If user is NOT allowed multiple active needs...
                user_needs = EducationalNeed.objects.filter(user=request.user)
                if any([need.is_active for need in user_needs]):
                    pass  # Do nothing if any of the needs is activated already
                else:
                    educational_need.is_active = True
            # Save model data in db.
            educational_need.save()

            # Redirect after submitting the form
            return redirect('view_profile')
    # If request is not POST, create empty form.
    else:
        if extended:
            form = EducationalNeedExtendedForm()
        else:
            form = EducationalNeedForm()

    # Check if user profile has required information for adding a need
    # It will be False if any of the fields is blank or null
    profile_complete = all([request.user.first_name, request.user.last_name,
                           request.user.email, request.user.profile.birth_date,
                           request.user.profile.mobile_number, request.user.profile.city,
                           request.user.profile.state, request.user.profile.country])

    # Create context dictionary which can be accessed in template
    context = {'form': form, 'profile_complete': profile_complete, 'is_extended': extended}
    template = 'educational_need/form_view.html'
    return render(request, template, context)


@login_required
def edit_need(request, pk):
    """Returns a view for editing EducationalNeed objects and handles POST
    requests submitted through the form."""
    educational_need = get_object_or_404(EducationalNeed, pk=pk)

    if educational_need.extended:
        extended = True
    else:
        extended = False

    if educational_need.closed:
        raise Http404("This need has been closed!")
    # If request method is POST, process form data.
    if request.method == 'POST':
        # Collect data from the form.
        if extended:
            form = EducationalNeedExtendedForm(request.POST, request.FILES, instance=educational_need)
        else:
            form = EducationalNeedForm(request.POST, request.FILES, instance=educational_need)
        # If form data is valid, process data and save.
        if form.is_valid():
            form.save()
            # Redirect after submitting the form
            return redirect('view_profile')
    # If request is not POST, create empty form.
    else:
        if extended:
            form = EducationalNeedExtendedForm(instance=educational_need)
        else:
            form = EducationalNeedForm(instance=educational_need)

    # Check if user profile has required information for adding a need
    # It will be False if any of the fields is blank or null
    profile_complete = all([request.user.first_name, request.user.last_name,
                           request.user.email, request.user.profile.birth_date,
                           request.user.profile.mobile_number, request.user.profile.city,
                           request.user.profile.state, request.user.profile.country])

    # Create context dictionary which can be accessed in template
    context = {'form': form, 'profile_complete': profile_complete, 'is_extended': extended}
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
    if educational_need.user != request.user:
        raise Http404('You do not have permission to edit this need!')
    if educational_need.closed:
        raise Http404('This need has been closed!')
    if educational_need.is_active:
        raise Http404('This need is already active!')

    user_profile = educational_need.user.profile
    if user_profile.multiple_needs:
        # If user is allowed multiple active needs...
        educational_need.is_active = True
        educational_need.save()
    else:
        # If user is NOT allowed multiple active needs...
        user_needs = EducationalNeed.objects.filter(user=educational_need.user)
        for need in user_needs:
            # Deactivate all needs first.
            need.is_active = False
            need.save()
        # Finally, activate only the need which was requested.
        educational_need.is_active = True
        educational_need.save()
    return redirect('view_profile')


@login_required
def deactivate_need(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if educational_need.user != request.user:
        raise Http404('You do not have permission to edit this need!')
    if educational_need.closed:
        raise Http404('This need has been closed!')
    if not educational_need.is_active:
        raise Http404('This need is already inactive!')

    educational_need.is_active = False
    educational_need.save()
    return redirect('view_profile')
