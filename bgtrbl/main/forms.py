from django import forms

from .models import UserProfile

class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
