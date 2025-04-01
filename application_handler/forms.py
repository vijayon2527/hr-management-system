from django import forms
from users.models import User
from django_select2.forms import Select2MultipleWidget
from job.models import Skill
from applicant.models import Applicant
from super_admin.models import Industry
from users.models import User
from applicant.models import Applicant
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "mobile")


class ApplicantForm(forms.ModelForm):
    industry = forms.ModelChoiceField(
        queryset=Industry.objects.all(),
        empty_label="Select an Industry",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Please select the relevant industry from the list."
    )
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'form-control select2'}),
        required=False
    )
    bio = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            industry_name = self.instance.extra_fields.get("category")
            if industry_name:
                try:
                    industry_instance = Industry.objects.get(name=industry_name)
                    self.fields['industry'].initial = industry_instance
                except Industry.DoesNotExist:
                    pass
                
    class Meta:
        model = Applicant
        fields = ["resume", #("industry", "resume")
                  "bio",
                  "current_job_title",
                  "skills",
                  "linkedin_profile",
                  "github_profile",
                  "portfolio_website",
                  "experience_level",
                  "years_of_experience",
                  "highest_education",
                  "is_available_for_work",
                  "willing_to_relocate",
                  "desired_salary",
                  "notice_period",
                  ]
        widgets = {
            "applicant_type": forms.Select(attrs={"class": "form-control"}),
            "experience_level": forms.Select(attrs={"class": "form-control"}),
            "highest_education": forms.Select(attrs={"class": "form-control"}),
            "notice_period": forms.Select(attrs={"class": "form-control"}),
            "desired_salary": forms.Select(attrs={"class": "form-control"}),
            "years_of_experience": forms.Select(attrs={"class": "form-control"}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "linkedin_profile": forms.URLInput(attrs={"class": "form-control"}),
            "github_profile": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio_website": forms.URLInput(attrs={"class": "form-control"}),
            "is_available_for_work": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "willing_to_relocate": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }