import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(UserCreationForm):

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'A user with that email already exists.')
        return cleaned_data


class UserCompletionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(UserCompletionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class ProfileCompletionForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('is_volunteer', 'organization_id', 'gender', 'birth_date', 'mobile_number',
                  'country', 'state', 'city', 'about', 'image')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileCompletionForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['birth_date'].required = True
        self.fields['mobile_number'].required = True
        self.fields['country'].required = True
        self.fields['state'].required = True
        self.fields['about'].required = True

    def clean(self):
        cleaned_data = super(ProfileCompletionForm, self).clean()
        birth_date = cleaned_data['birth_date']
        birth_year = birth_date.year
        current_year = datetime.datetime.today().year
        max_year = current_year - 6
        if birth_year > max_year:
            self.add_error('birth_date', 'You must be at least 6 years old!')
        if cleaned_data['is_volunteer'] and not cleaned_data['organization_id']:
            self.add_error('organization_id', 'You must select an orgnization if you want to be a volunteer.')
        return cleaned_data


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'A user with that email already exists.')
        return cleaned_data


class OrganizationUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super(OrganizationUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].required = True

    def clean(self):
        cleaned_data = super(OrganizationUserForm, self).clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'A user with that email already exists.')
        return cleaned_data


class ProfileForm(forms.ModelForm):
        
    class Meta:
        model = Profile
        fields = ('middle_name', 'gender', 'birth_date', 'mobile_number', 'hide_mobile_number', 'phone_number',
                  'hide_phone_number', 'country', 'state', 'zip_code', 'city', 'district',
                  'about', 'image', )
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['birth_date'].required = True
        self.fields['mobile_number'].required = True
        self.fields['country'].required = True
        self.fields['state'].required = True
        self.fields['about'].required = True

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        birth_date = cleaned_data['birth_date']
        birth_year = birth_date.year
        current_year = datetime.datetime.today().year
        max_year = current_year - 6
        if birth_year > max_year:
            self.add_error('birth_date', 'You must be at least 6 years old!')
        return cleaned_data


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'mobile_number',
            'mobile_number_2',
            'phone_number',
            'phone_number_2',
            'fax_number',
            'additional_contact_details',
            'country',
            'state',
            'zip_code',
            'city',
            'district',
            'organization_address',
            'about',
            'image',
        )

    def __init__(self, *args, **kwargs):
        super(OrganizationProfileForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].required = True
        self.fields['country'].required = True
        self.fields['state'].required = True
        self.fields['about'].required = True



class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password',)


class OrganizationSignupForm(UserCreationForm):

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(OrganizationSignupForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'Account with that username already exists.')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'Account with that email already exists.')
        return cleaned_data


class OrganizationCompletionForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'organization_name',
            'image',
            'phone_number',
            'phone_number_2',
            'mobile_number',
            'mobile_number_2',
            'fax_number',
            'additional_contact_details',
            'country',
            'state',
            'city',
            'district',
            'zip_code',
            'organization_address',
            'about',
            )

    def __init__(self, *args, **kwargs):
        super(OrganizationCompletionForm, self).__init__(*args, **kwargs)
        self.fields['organization_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['country'].required = True
        self.fields['state'].required = True
        self.fields['zip_code'].required = True
        self.fields['organization_address'].required = True
        self.fields['about'].required = True


class VolunteerApplicationForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'is_volunteer',
            'organization_id',
        )

    def __init__(self, *args, **kwargs):
        super(VolunteerApplicationForm, self).__init__(*args, **kwargs)
        self.fields['is_volunteer'].required = True
        self.fields['organization_id'].required = True
