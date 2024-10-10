from django import forms
from users.models import User
from employer.models import Employer

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = [
            'user',
            'created_at',
            'updated_at',
            'is_verified',
            'verified_at'
        ]

class EmployerUserProfileForm(forms.ModelForm):
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