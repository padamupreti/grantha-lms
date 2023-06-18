from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import LMSUser


class LMSUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=40, label='First Name')
    last_name = forms.CharField(
        max_length=40, label='Last Name')
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = LMSUser

    def save(self, commit=True):
        user = super(LMSUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
