from django import template
from bgtrbl.apps.trblcms.forms import ArticleModelForm
from bgtrbl.apps.trblcms.models import Article
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# @depr
def get_article_form(context):
    # @todo change it to the Article specific form checking
    #article = get_object_or_404(models.Article, slug=slug) if slug else None
    #print(slug, article)
    return context

# @depr
def get_articles(content_type, pk):
    if ContentType.objects.filter(model=content_type).exists():
        articles = Article.objects.filter(sequel=pk)
    return{'articles': articles}


register.inclusion_tag('trblcms/templatetags/_article_form.html', takes_context=True)(get_article_form)
register.inclusion_tag('trblcms/templatetags/_articles.html')(get_articles)
