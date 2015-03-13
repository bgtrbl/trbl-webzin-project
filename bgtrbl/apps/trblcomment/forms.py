from django import forms
from .models import Comment

#from ckeditor.widgets import CKEditorWidget


# for security reason(when changing server state, use POST other than GET)
# parent_thread is in the form
class CommentForm(forms.Form):
    text = forms.CharField(max_length=500, required=True)

    #class Meta:
        #model = Comment
        #fields = ('author', 'body')
        #widgets = {'parent_thread': forms.HiddenInput()}
