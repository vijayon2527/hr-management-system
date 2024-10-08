from django import forms
from users.models import User
from applicant.models import Applicant

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = [
            'user',
            'skills',
            'created_at',
            'updated_at'
        ]

class ApplicantUserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }),
        input_formats=['%Y-%m-%d'],
    )
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'date_of_birth',
                  'address_line_1',
                  'address_line_2',
                  'city',
                  'state',
                  'country',
                  'postal_code',
                  
        ]