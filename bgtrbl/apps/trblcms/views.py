from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


from .models import Article
from .forms import ArticleModelForm, CkeditorTestForm


def formTest(request):
    if request.method == 'POST':
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            output = ''
            for k, v in form.cleaned_data.items():
                output += "{}: {}<br />".format(k, v)
            return HttpResponse("Succeed<br />"+output)
    else:
        # initial attr gives a prepopulated form
        form = ArticleModelForm(initial={'category': None})
    return render(request, 'trblcms/form_test.html', {'form': form})


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


def addOrEditArticle(request, slug=None):
    article = get_object_or_404(Article, slug=slug) if slug else None     # 404 exception(accessing with weird slug) filtered
    form = ArticleModelForm(initial={'category': None}, instance=article)
    return render(request, 'trblcms/add_or_edit_article.html', {'form': form})


def saveArticle(request):
    if request.method == 'POST':
        article, created = Article.objects.get_or_create(slug=request.POST['slug'])
        # @? do I need to check for slug clash(if created)? or uuslug already have taken
        # care of it before?
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

    
