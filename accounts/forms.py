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
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
        
    class Meta:
        model = Profile
        fields = ('birth_date', 'mobile_number', 'phone_number',
                  'country', 'state', 'zip_code', 'city', 'district', 'about')
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password',)
