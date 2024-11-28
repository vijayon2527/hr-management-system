from django import forms
from .models import Industry, FunctionalArea, Role
from users.models import User
from applicant.models import Applicant

class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ['name', 'description', 'is_active']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Industry name cannot be blank.")
        return name


class FunctionalAreaForm(forms.ModelForm):
    class Meta:
        model = FunctionalArea
        fields = ['industry', 'name', 'description', 'is_active']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Functional area name cannot be blank.")
        return name


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['functional_area', 'name', 'description', 'is_active']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Role title cannot be blank.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        functional_area = cleaned_data.get('functional_area')
        name = cleaned_data.get('name')

        # Additional validation: Check if the role already exists in the functional area
        if functional_area and Role.objects.filter(functional_area=functional_area, name=name).exists():
            raise forms.ValidationError(f"A role with the name '{name}' already exists in the selected functional area.")

        return cleaned_data

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

    class Meta:
        model = Applicant
        fields = ("industry", "resume")
