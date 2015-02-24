from django import template
from bgtrbl.apps.trblcms.forms import ArticleModelForm, CommentModelForm

register = template.Library()


def get_article_form(context):
    # @todo change it to the Article specific form checking
    if not context.has_key('article_form'):
        context['article_form'] = ArticleModelForm(initial={'category': None})
    #article = get_object_or_404(models.Article, slug=slug) if slug else None
    #print(slug, article)
    return context


def get_comment_form(context):
    context['comment_form'] = CommentModelForm()
    return context


register.inclusion_tag('trblcms/_article_form.html', takes_context=True)(get_article_form)
register.inclusion_tag('trblcms/_comment_form.html', takes_context=True)(get_comment_form)
