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
    job_title = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}), required=True)
    experience = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), required=False)
    no_of_openings = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.Select(choices=Job.COUNTRY_CHOICES, attrs={'class': 'form-control'}))
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    functional_area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    industry = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Job
        # fields = "__all__"
        exclude = ('user',
                   'slug', 
                   'skills',
                   'uploaded_by', 
                   'published_at', 
                   'employement_type', 
                   'visit_count', 
                   'updated_at', 
                   'job_applied_count',
                   )

class JobApplicantUserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields = (
            'name',
            'mobile',
        )