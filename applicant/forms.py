from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from applicant.models import Applicant

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = [
            'user',
            'skills',
            'created_at',
            'updated_at',
            'resume'
        ]
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary < 0:
            raise ValidationError("Salary cannot be negative.")
        return salary

    # Example of another field validator for the 'bio' field, if needed
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 500:
            raise ValidationError("Bio cannot exceed 500 characters.")
        return bio

class ApplicantUserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }),
        input_formats=['%Y-%m-%d'],
    )
    class Meta:
        model = User
        fields = ['profile_pic',
                  'first_name',
                  'last_name',
                  'date_of_birth',
                  'address_line_1',
                  'address_line_2',
                  'city',
                  'state',
                  'country',
                  'postal_code',
                  
        ]


class ApplicantResumeForm(forms.ModelForm):
    resume = forms.FileField(required=True)
    class Meta:
        model = Applicant
        fields = ['resume']