from django import forms
from django.contrib import admin
from .models import Article
from ckeditor.widgets import CKEditorWidget


class ArticleModelForm(forms.ModelForm):
    slug = forms.CharField(max_length=200, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Article
        exclude = ['created_at', 'modified_at']
        widgets = {'category': forms.HiddenInput()}


class CkeditorTestForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')


#class ArticleAdminForm(forms.ModelForm):
