from django import forms
from django.contrib import admin
from .models import Article, Sequel
from ckeditor.widgets import CKEditorWidget


class ArticleModelForm(forms.ModelForm):
    slug = forms.CharField(max_length=200, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        exclude = ['created_at', 'modified_at', 'child_thread', 'user']
        #widgets = {'category': forms.HiddenInput()}


class SequelModelForm(forms.ModelForm):
    slug = forms.CharField(max_length=200, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sequel
        exclude = ['child_thread', 'user']
