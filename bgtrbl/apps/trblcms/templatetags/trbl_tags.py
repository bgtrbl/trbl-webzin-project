from django import template
from bgtrbl.apps.trblcms.forms import ArticleModelForm, CommentModelForm
from bgtrbl.apps.trblcms.models import Comment

register = template.Library()


def get_article_form(context):
    # @todo change it to the Article specific form checking
    if not context.has_key('article_form'):
        context['article_form'] = ArticleModelForm(initial={'category': None})
    #article = get_object_or_404(models.Article, slug=slug) if slug else None
    #print(slug, article)
    return context


# temporary name for commented object
def get_comment_form(object_id):
    return {'comment_form': CommentModelForm(), 'object_id': object_id}


def get_comments(object_id):
    return {'comments': Comment.objects.filter(article=object_id)}


register.inclusion_tag('trblcms/_article_form.html', takes_context=True)(get_article_form)
register.inclusion_tag('trblcms/_comment_form.html')(get_comment_form)
register.inclusion_tag('trblcms/_comments.html')(get_comments)
