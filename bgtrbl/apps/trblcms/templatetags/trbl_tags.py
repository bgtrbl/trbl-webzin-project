from django import template
from bgtrbl.apps.trblcms.forms import ArticleModelForm, CommentForm
from bgtrbl.apps.trblcms.models import Comment, Article
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# @depr
def get_article_form(context):
    # @todo change it to the Article specific form checking
    #article = get_object_or_404(models.Article, slug=slug) if slug else None
    #print(slug, article)
    return context


# temporary name for commented object
# @todo change the name of the object_id in conext dict to thread_id(in
# the template too)
# @idea: get commented_item_id, commented_item_type and return a form
# prepoplutated with the corresponding thread_id via accessing the
# child_thread attr of the CommentedItemMixin
# possible solution: contenttype framework
def get_comment_form(content_type, pk):
    # content_type goes to form's action value to saveComment view via url
    return {'comment_form': CommentForm(),
            'content_type': content_type,
            'pk': pk,
            }


def get_comments(content_type, pk):
    if ContentType.objects.filter(model=content_type).exists():
        model_class = ContentType.objects.get(model=content_type).model_class()
        child_thread = model_class.objects.get(id=pk).child_thread
        return {'comments': Comment.objects.filter(parent_thread=child_thread),
            }
    print("something is wrong")

# @depr
def get_articles(content_type, pk):
    if ContentType.objects.filter(model=content_type).exists():
        articles = Article.objects.filter(sequel=pk)
    return{'articles': articles}


register.inclusion_tag('trblcms/templatetags/_article_form.html', takes_context=True)(get_article_form)
register.inclusion_tag('trblcms/templatetags/_comment_form.html')(get_comment_form)
register.inclusion_tag('trblcms/templatetags/_comments.html')(get_comments)
register.inclusion_tag('trblcms/templatetags/_articles.html')(get_articles)
