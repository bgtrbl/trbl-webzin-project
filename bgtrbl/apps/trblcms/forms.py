from django import forms
from django.contrib import admin
from .models import Article, Comment
from ckeditor.widgets import CKEditorWidget


class ArticleModelForm(forms.ModelForm):
    slug = forms.CharField(max_length=200, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Article
        exclude = ['created_at', 'modified_at']
        #widgets = {}


class CkeditorTestForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')


#class ArticleAdminForm(forms.ModelForm):


# for security reason(when changing server state, use POST other than GET)
# parent_thread is in the form
class CommentForm(forms.Form):
    author = forms.CharField(max_length=100, required=True)
    text = forms.CharField(max_length=500, required=True)

    #class Meta:
        #model = Comment
        #fields = ('author', 'body')
        #widgets = {'parent_thread': forms.HiddenInput()}
