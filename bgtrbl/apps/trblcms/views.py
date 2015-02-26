from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

# for comment saving
from django.contrib.contenttypes.models import ContentType

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article, Comment
from .forms import ArticleModelForm, CkeditorTestForm, CommentForm


def ckeditorTest(request):
    if request.method == 'POST':
        form = CkeditorTestForm(request.POST)
        if form.is_valid():
            return HttpResponse("good")
    else:
        form = CkeditorTestForm()
    return render(request, 'trblcms/ckeditor_test.html', {'form': form})


class ArticleListView(ListView):
    model = Article
    template_name = 'trblcms/article_list.html'

    # context configuring
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'trblcms/article_detail.html'

    # context configuring
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @? change it to use the trbl_tags?
def addOrEditArticle(request, slug=None):
    article = get_object_or_404(Article, slug=slug) if slug else None     # 404 exception(accessing with weird slug) filtered
    form = ArticleModelForm(instance=article)
    return render(request, 'trblcms/add_or_edit_article.html', {'article_form': form})


def saveArticle(request):
    if request.method == 'POST':
        article, created = Article.objects.get_or_create(slug=request.POST['slug'])
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            # @todo user authorization needed (if the user changed the category
            # or slug to purposly change other Articles, than django must know)
            form.save()
            # article slug or form slug
            return redirect('trblcms:article_detail', slug=article.slug)
        if created:
            article.delete()
        return redirect('trblcms:edit_article', slug=request.POST['slug']) # @!
    return redirect('main:home')


# @! security flaws
# @? id or slug?
# @todo eventually pk has to go, and from would pass things in post to deal
# with redirection
# @idea or maybe getting next="url" whith GET method also would be nice...
def saveComment(request, content_type, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and ContentType.objects.filter(model=content_type).exists():
            model_class = ContentType.objects.get(model=content_type).model_class()
            parent_thread = model_class.objects.get(id=pk).child_thread
            Comment.objects.create(author=form.cleaned_data['author'], text=form.cleaned_data['text'], parent_thread=parent_thread)
        else: print("form valid({}); content type({}) isn't matching".format(form.is_valid(), content_type))
    # @? comment redirection... where to go if fails?
    # @todo support many content type that inherits CommentedItemMixin
    return redirect('trblcms:article_detail', slug=Article.objects.get(id=pk).slug)
