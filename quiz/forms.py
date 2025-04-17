from django import forms
from .models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_active', 'is_timed', 'duration']

    # You can set custom validation or messages if needed
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            raise forms.ValidationError("This field is required.")
        return duration
