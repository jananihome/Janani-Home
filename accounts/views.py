import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from educational_need.models import EducationalNeed

from .forms import SignupForm, UserCompletionForm, ProfileCompletionForm
from .forms import ProfileForm, UserForm, PasswordChangeForm
from .forms import OrganizationSignupForm, OrganizationCompletionForm
from .forms import OrganizationUserForm, OrganizationProfileForm
from .forms import VolunteerApplicationForm

from .models import Profile
from .models import State

from .tokens import account_activation_token as activation_token


def send_email(subject, message, toemails):
    email = EmailMessage(subject, message, to=toemails)
    email.send()

def send_new_registration_email(request, profile):
    current_site = get_current_site(request)
    subject = 'New User registration on Janani Home'
    message = render_to_string('accounts/new_user_email.html', {
                'domain': current_site.domain,
                'profile': profile,
            })
    if profile.is_organization:
        subject = 'New NGO registration on Janani Home'
        message = render_to_string('accounts/ngo_approval_email.html', {
                'domain': current_site.domain,
                'profile': profile,
            })
    elif profile.is_volunteer:
        subject = 'New Volunteer registration on Janani Home'
        message = render_to_string('accounts/new_volunteer_email.html', {
                'domain': current_site.domain,
                'profile': profile,
            })
    toemails = [u.email for u in User.objects.filter(is_staff=True)]
    email = EmailMessage(subject, message, to=toemails)
    email.send()

def signup(request):
    if request.user.is_authenticated():
        return redirect('view_profile')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                message = render_to_string('accounts/activation_email.html', {
                    'user': user, 'domain': get_current_site(request),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': activation_token.make_token(user),
                })
                send_email(
                    subject='Activate your account on Janani Care',
                    message=message,
                    toemails=[form.cleaned_data.get('email')],
                    )
                return render(request, 'accounts/activation_pending.html')
        else:
            form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':
        user_form = UserCompletionForm(request.POST, instance=user)
        profile_form = ProfileCompletionForm(request.POST, request.FILES,
                                             instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user.is_active = True
            user_form.save()
            profile_form.save()
            send_new_registration_email(request, user.profile)
            login(request, user)
            return render(request, 'accounts/activation_completed.html')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserCompletionForm()
        profile_form = ProfileCompletionForm()
        if user is not None and activation_token.check_token(user, token):
            pass
        else:
            return HttpResponse('Activation link is invalid!')
    return render(request, 'accounts/complete_registration.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request):
    context = {}
    if request.user.profile.is_organization:
        template = 'accounts/ngo_profile.html'
    else:
        if request.method == 'POST':
            volunteer_form = VolunteerApplicationForm(request.POST, instance=request.user.profile)
            if volunteer_form.is_valid():
                volunteer_form.save()
                
                # Send email to admins
                current_site = get_current_site(request)
                subject = 'New Volunteer application on Janani Home'
                message = render_to_string('accounts/new_volunteer_email.html', {
                'domain': current_site.domain,
                'profile': request.user.profile,
                })
                toemails = [u.email for u in User.objects.filter(is_staff=True)]
                email = EmailMessage(subject, message, to=toemails)
                email.send()
                messages.info(request, _('Thank you! You will receive a message when NGO reviews your application.'))
                return redirect('view_profile')
        else:
            volunteer_form = VolunteerApplicationForm(instance=request.user.profile)
            educational_needs = EducationalNeed.objects.filter(user=request.user)
            template = 'accounts/view_profile.html'
            context = {'educational_needs': educational_needs,'volunteer_form': volunteer_form}
    return render(request, template, context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.user.profile.is_organization:
        return redirect('update_ngo_profile')
    if request.method == 'POST':
        current_email = request.user.email
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            if current_email != user.email:
                profile.unconfirmed_email = user.email
                user.email = current_email

                # Send activation email
                current_site = get_current_site(request)
                message = render_to_string(
                    'accounts/email_confirmation_email.html', {
                        'user': user, 'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk))})
                send_email(
                    subject='Confirm your new email address on Janani Care',
                    message=message,
                    toemails=[profile.unconfirmed_email],
                    )

                # Display message for the user
                messages.warning(request, _(
                    ''' Your have requested an email change to %s! We have just
                    sent you a message to %s with a confirmation link inside.
                    You have to click the link in the message to confirm your
                    new email address. If you don't click the link, %s will
                    continue to be your only active email address. If for some
                    reason the message doesn't arrive, try to change the email
                    again or contact administration.'''
                    % (profile.unconfirmed_email, profile.unconfirmed_email,
                       current_email)
                ))
            user.save()
            profile.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('update_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def update_ngo_profile(request):
    if not request.user.profile.is_organization:
        return redirect('update_profile')
    if request.method == 'POST':
        current_email = request.user.email
        user_form = OrganizationUserForm(request.POST, instance=request.user)
        profile_form = OrganizationProfileForm(request.POST, request.FILES,
                                               instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            if current_email != user.email:
                profile.unconfirmed_email = user.email
                user.email = current_email

                # Send activation email
                current_site = get_current_site(request)
                message = render_to_string(
                    'accounts/email_confirmation_email.html', {
                        'user': user, 'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk))})
                send_email(
                    subject='Confirm your new email address on Janani Care',
                    message=message,
                    toemails=[profile.unconfirmed_email]
                )

                messages.warning(request, _(
                    ''' Your have requested an email change to %s! We have just
                    sent you a message to %s with a confirmation link inside.
                    You have to click the link in the message to confirm your
                    new email address. If you don't click the link, %s will
                    continue to be your only active email address. If for some
                    reason the message doesn't arrive, try to change the email
                    again or contact administration.'''
                    % (profile.unconfirmed_email, profile.unconfirmed_email,
                       current_email)
                ))
            user.save()
            profile.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('update_ngo_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = OrganizationUserForm(instance=request.user)
        profile_form = OrganizationProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_ngo_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@transaction.atomic
def confirm_new_email(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.email = user.profile.unconfirmed_email
        user.profile.unconfirmed_email = None
        user.save()
        user.profile.save()
        messages.success(request, _('Your new email was successfully confirmed!'))
    else:
        return HttpResponse('Email activation link is invalid!')

    return redirect('view_profile')

@login_required
@transaction.atomic
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def StateAjaxView(request):
    """function to render the states accourding to the city passed"""
    try:
        country_id = request.GET.get('country_id')
        return HttpResponse(
            json.dumps(tuple(i for i in State.objects.filter(
                        country_id=country_id).values('name', 'id', 'code'))),
            content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps([]),content_type='application/json')


def organization_signup(request):
    if request.user.is_authenticated():
        return redirect('view_profile')
    else:
        if request.method == 'POST':
            form = OrganizationSignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                message = render_to_string(
                    'accounts/organization_activation_email.html', {
                        'user': user, 'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': activation_token.make_token(user),
                    })
                send_email(
                    subject='Activate your NGO account on Janani Care',
                    message=message,
                    toemails=[form.cleaned_data.get('email')]
                )
                return render(request, 'accounts/activation_pending.html')
        else:
            form = OrganizationSignupForm()
        return render(
            request,
            'accounts/organization_signup.html',
            {'form': form})


def activate_organization(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':
        form = OrganizationCompletionForm(request.POST, request.FILES,
                                          instance=user.profile)
        if form.is_valid():
            user.is_active = True
            user.profile.is_organization = True
            user.profile.active = False  # NGOs need manual approval by admin
            user.profile.multiple_needs = True  # NGOs can add multiple needs by default
            form.save()
            user.save()
            current_site = get_current_site(request)
            send_new_registration_email(request, user.profile)
            login(request, user)
            return render(request, 'accounts/activation_completed.html')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = OrganizationCompletionForm()
        if user is not None and activation_token.check_token(user, token):
            pass
        else:
            return HttpResponse('Activation link is invalid!')
    return render(
        request,
        'accounts/complete_organization_registration.html',
        {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def ngo_approval(request, pk):
    ngo = get_object_or_404(Profile, pk=pk)
    user = get_object_or_404(User, pk=ngo.user.pk)
    return render(
        request,
        'accounts/ngo_approval.html',
        {'ngo': ngo, 'user': user})


@user_passes_test(lambda u: u.is_superuser)
def approve_ngo(request, pk):
    ngo = get_object_or_404(Profile, pk=pk)
    ngo.active = True
    ngo.save()
    # Send email to NGO
    send_email(
        subject='Your NGO account was approved',
        message=render_to_string('accounts/ngo_approved_email.html'),
        toemails=[ngo.user.email]
    )
    messages.info(request, _('Profile was approved. NGO will receive an email\
                             with this information.'))
    return redirect('ngo_approval', ngo.pk)


@user_passes_test(lambda u: u.is_superuser)
def reject_ngo(request, pk):
    ngo = get_object_or_404(Profile, pk=pk)
    ngo.active = False
    ngo.save()
    send_email(
        subject='Your NGO account was rejected',
        message=render_to_string('accounts/ngo_rejected_email.html'),
        toemails=[ngo.user.email]
    )
    messages.info(request, _('Profile was rejected. NGO will receive an email\
                             with this information.'))
    return redirect('ngo_approval', ngo.pk)


@login_required
def volunteer_approval(request, pk):
    admin_profile = get_object_or_404(Profile, pk=request.user.pk)
    volunteer = get_object_or_404(Profile, pk=pk)
    user = get_object_or_404(User, pk=volunteer.user.pk)

    if request.user.is_superuser or admin_profile == volunteer.organization_id:
        return render(
            request,
            'accounts/volunteer_approval.html',
            {'volunteer': volunteer, 'user': user})
    else:
        return HttpResponse('You don\'t have access to this page!')


@login_required
def approve_volunteer(request, pk):
    admin_profile = get_object_or_404(Profile, pk=request.user.pk)
    volunteer = get_object_or_404(Profile, pk=pk)

    if request.user.is_superuser or admin_profile == volunteer.organization_id:
        volunteer.approved_volunteer = True
        volunteer.volunteer_start_date = timezone.now()
        volunteer.volunteer_cancellation_date = None
        volunteer.save()
        # Send email to Volunteer
        send_email(
            subject='Your volunteer application was approved by NGO',
            message=render_to_string('accounts/volunteer_approved_email.html'),
            toemails=[volunteer.user.email]
        )
    messages.info(request, _('Profile was approved. Volunteer will receive an email\
                             with this information.'))
    return redirect('volunteer_approval', volunteer.pk)


@login_required
def reject_volunteer(request, pk):
    volunteer = get_object_or_404(Profile, pk=pk)
    volunteer.approved_volunteer = False
    volunteer.volunteer_cancellation_date = timezone.now()
    volunteer.save()
    send_email(
        subject='Your volunteer application was rejected by NGO',
        message=render_to_string('accounts/volunteer_rejected_email.html'),
        toemails=[volunteer.user.email],
    )
    messages.info(request, _('Profile was rejected. Volunteer will receive an email\
                             with this information.'))
    return redirect('volunteer_approval', volunteer.pk)

@login_required
def volunteer_cancellation(request, pk):
    volunteer = get_object_or_404(Profile, pk=pk)
    volunteer.is_volunteer = False
    volunteer.approved_volunteer = False
    volunteer.volunteer_cancellation_date = timezone.now()
    # Send email to NGO
    send_email(
        subject='Volunteer cancelled work with your organization',
        message='Volunteer {} ({}) opted out from your organization.'.format(volunteer.get_full_name(), volunteer),
        toemails=[volunteer.organization_id.user.email]
    )
    messages.info(request, _('You have cancelled your cooperation with {}. If you wish, you can now apply to other NGO.'.format(volunteer.organization_id)))
    volunteer.organization_id = None
    volunteer.save()
    return redirect('view_profile')
