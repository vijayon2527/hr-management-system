from tinymce.widgets import TinyMCE
from django import forms
from job.models import Job, User
from job.models import Skill

class AddSkill(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}))

    class Meta:
        model = Skill
        fields = ("name",)

class CreateJobForm(forms.ModelForm):
    application_deadline = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
        }),
        input_formats=['%Y-%m-%d'],
    )
    class Meta:
        model = Job
        fields = [
            'job_title',
            'role',
            'job_description',
            'min_experience',
            'max_experience',
            'min_salary',
            'max_salary',
            'salary_currency',
            'salary_period',
            'qualification',
            'no_of_openings',
            'industry',
            'functional_area',
            'employment_type',
            'country',
            'state',
            'city',
            'place',
            'benefits',
            'perks',
            'application_deadline',
            'remote_possible',
            'is_flexible',
            'visa_sponsorship',
            'relocation_support',
        ]

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')
        min_experience = cleaned_data.get('min_experience')
        max_experience = cleaned_data.get('max_experience')

        # Validate salary range
        if min_salary is not None and max_salary is not None:
            if min_salary > max_salary:
                self.add_error('max_salary', 'Minimum salary cannot be greater than maximum salary.')

        # Validate experience range
        if min_experience is not None and max_experience is not None:
            if min_experience > max_experience:
                self.add_error('max_experience', 'Minimum experience cannot be greater than maximum experience.')

        return cleaned_data
    
class JobApplicantUserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields = (
            'name',
            'mobile',
        )