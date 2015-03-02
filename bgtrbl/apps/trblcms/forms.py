from django import forms
from django.contrib import admin
from .models import Article, Comment, Sequel
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


class CkeditorTestForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')


#class ArticleAdminForm(forms.ModelForm):


# for security reason(when changing server state, use POST other than GET)
# parent_thread is in the form
class CommentForm(forms.Form):
    text = forms.CharField(max_length=500, required=True)

    #class Meta:
        #model = Comment
        #fields = ('author', 'body')
        #widgets = {'parent_thread': forms.HiddenInput()}
