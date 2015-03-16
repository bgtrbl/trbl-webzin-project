from django import template
from bgtrbl.apps.trblcomment.forms import CommentForm
from bgtrbl.apps.trblcomment.models import Comment
from django.contrib.contenttypes.models import ContentType


register = template.Library()


# temporary name for commented object
# @todo change the name of the object_id in conext dict to thread_id(in
# the template too)
# @idea: get commented_item_id, commented_item_type and return a form
# prepoplutated with the corresponding thread_id via accessing the
# child_thread attr of the CommentedItemMixin
# possible solution: contenttype framework
def get_comment_form(context):
    # content_type goes to form's action value to saveComment view via url
    return {'comment_form': CommentForm(),
            'object': context['object'],
            'user': context['user'],
            }


# 고쳐야됨...
def get_comments(thread_id):
    return {'comments': Comment.objects.filter(parent_thread=thread_id),}


register.inclusion_tag('trblcomment/templatetags/_comment_form_ajax.html', takes_context=True)(get_comment_form)
register.inclusion_tag('trblcomment/templatetags/_comments_ajax.html')(get_comments)
