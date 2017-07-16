from django import forms
# Models imports
from .models import EducationalNeed
from comment.models import Comment

class EducationalNeedForm(forms.ModelForm):
    """Defines a front-end form for EducationalNeed model."""
    class Meta:
        model = EducationalNeed
        fields = (
            'permanent_address',
            'current_address',
            'college_school_address',
            'college_school_contact_details',
            'amount_required',
            'requirement_description',
            'communication_mode',)


class UserContactForm(forms.Form):
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
