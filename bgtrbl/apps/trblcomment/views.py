from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

# comment saving by ContentType
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from .models import Comment
from .forms import CommentForm

import json


# @! security flaws
# @todo eventually pk has to go, and from would pass things in post to deal
# with redirection
# @idea or maybe getting next="url" whith GET method also would be nice...
def saveComment(request, content_type, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and ContentType.objects.filter(model=content_type).exists():
            commented_item = ContentType.objects.get(model=content_type).model_class().objects.get(id=pk)
            Comment.objects.create(user=request.user,
                    text=form.cleaned_data['text'],
                    parent_thread=commented_item.child_thread)
        else:
            # @404
            print("form valid({}); content type({}) isn't matching".format(form.is_valid(), content_type))
    # @? comment redirection... where to go if fails?
    # @todo support many content type that inherits CommentedItemMixin
    return redirect(commented_item.get_absolute_url())

def addComment(request):
    print("called by", request.user.username)
    if 'comment_text' in request.GET:
        response_dict = {'comment_text': request.GET['comment_text']}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
