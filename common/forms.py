from django import forms
from users.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
