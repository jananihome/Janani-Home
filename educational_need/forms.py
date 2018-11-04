from datetime import datetime
from django import forms

from .models import EducationalNeed


class EducationalNeedForm(forms.ModelForm):
    """Defines a front-end form for EducationalNeed model."""
    class Meta:
        model = EducationalNeed
        fields = (
            'title',
            'permanent_address',
            'hide_permanent_address',
            'current_address',
            'hide_current_address',
            'additional_mobile_number',
            'hide_mobile_number',
            'additional_phone_number',
            'hide_phone_number',
            'college_school_address',
            'college_school_contact_details',
            'amount_required',
            'requirement_description',
            'youtube_url',
            'communication_mode',)


class EducationalNeedExtendedForm(forms.ModelForm):

    class Meta:
        model = EducationalNeed
        fields = (
            'title',
            'ext_first_name',
            'ext_middle_name',
            'ext_last_name',
            'ext_gender',
            'ext_birth_date',
            'ext_country',
            'ext_state',
            'ext_zip_code',
            'ext_city',
            'ext_district',
            'permanent_address',
            'hide_permanent_address',
            'current_address',
            'hide_current_address',
            'additional_mobile_number',
            'hide_mobile_number',
            'additional_phone_number',
            'hide_phone_number',
            'ext_email',
            'communication_mode',
            'college_school_address',
            'college_school_contact_details',
            'ext_about',
            'ext_image',
            'amount_required',
            'requirement_description',
            'youtube_url',
        )

        widgets = {
            'ext_birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EducationalNeedExtendedForm, self).__init__(*args, **kwargs)
        self.fields['ext_first_name'].required = True
        self.fields['ext_last_name'].required = True
        self.fields['ext_gender'].required = True
        self.fields['ext_birth_date'].required = True
        self.fields['ext_country'].required = True
        self.fields['ext_state'].required = True
        self.fields['ext_city'].required = True
        self.fields['ext_about'].required = True
        self.fields['title'].required = True
        self.fields['permanent_address'].required = True
        self.fields['additional_mobile_number'].required = True
        self.fields['college_school_address'].required = True
        self.fields['college_school_contact_details'].required = True
        self.fields['requirement_description'].required = True
        self.fields['communication_mode'].required = True

    def clean(self):
        cleaned_data = super(EducationalNeedExtendedForm, self).clean()
        ext_birth_date = cleaned_data['ext_birth_date']
        birth_year = ext_birth_date.year
        current_year = datetime.today().year
        max_year = current_year - 6
        if birth_year > max_year:
            self.add_error('ext_birth_date', 'Person must be at least 6 years old!')
        return cleaned_data


class UserContactForm(forms.Form):
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
