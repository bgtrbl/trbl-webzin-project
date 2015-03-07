from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

# comment saving by ContentType
from django.contrib.contenttypes.models import ContentType

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from .models import Article, Sequel, Category
from .forms import ArticleModelForm, SequelModelForm


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'trblcms/article_detail.html'

    # context configuring
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def addArticle(request):
    form = ArticleModelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        article.user = request.user
        article.save()
        form.save_m2m()
        return redirect(article.get_absolute_url())
    return render(request, 'trblcms/add_or_edit_article.html', {'article_form': form})


def editArticle(request, pk):
    article= get_object_or_404(Article, id=pk, user=request.user)
    form = ArticleModelForm(request.POST or None, instance=article)
    if request.method == 'POST' and form.is_valid():
        # @todo user authorization needed (if the user changed the category
        # or slug to purposly change other Articles, than django must know)
        article = form.save(commit=False)
        article.user = request.user
        article.save()
        form.save_m2m()
        return redirect(article.get_absolute_url())
    return render(request, 'trblcms/add_or_edit_article.html', {'article_form': form, 'pk': pk})


class SequelDetailView(DetailView):
    model = Sequel
    template_naem = 'trblcms/sequel_detail.html'


def addSequel(request):
    form = SequelModelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        sequel = form.save(commit=False)
        sequel.user = request.user
        sequel.save()
        return redirect(sequel.get_absolute_url())
    return render(request, 'trblcms/add_or_edit_sequel.html', {'sequel_form': form})


def editSequel(request, pk):
    sequel = get_object_or_404(Sequel, id=pk, user=request.user)
    form = SequelModelForm(request.POST or None, instance=sequel)
    if request.method == 'POST' and form.is_valid():
        sequel = form.save(commit=False)
        sequel.user = request.user
        sequel.save()
        return redirect(sequel.get_absolute_url())
    return render(request, 'trblcms/add_or_edit_sequel.html', {'sequel_form': form, 'pk': pk})


class SequelEditView(FormView):
    template_name = 'trblcms/sequel_edit.html'
    form_class = SequelModelForm
    # temp
    success_url = '/main/'

    #def form_valid(self, form):


class ArticleListView(ListView):
    model = Article
    template_name = 'trblcms/article_list.html'

    # context configuring
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
