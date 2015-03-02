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

from .models import Article, Comment, Sequel, Category
from .forms import ArticleModelForm, CkeditorTestForm, CommentForm, SequelModelForm


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'trblcms/article_detail.html'

    # context configuring
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @? change it to use the trbl_tags?
def addOrEditArticle(request, pk=None):
    article = get_object_or_404(Article, id=pk, user=request.user) if pk else None     # 404 exception(accessing with weird slug) filtered
    form = ArticleModelForm(instance=article)
    return render(request, 'trblcms/add_or_edit_article.html', {'article_form': form, 'pk': pk})


def saveOrUpdateArticle(request, pk=None):
    if request.method == 'POST':
        article, created = Article.objects.get_or_create(id=pk, user=request.user)
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            # @todo user authorization needed (if the user changed the category
            # or slug to purposly change other Articles, than django must know)
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            form.save_m2m()

            # article slug or form slug
            return redirect(article.get_absolute_url())
        if created:
            article.delete()
        return redirect('trblcms:edit_article', pk=pk) # @!
    return redirect('main:home')


class SequelDetailView(DetailView):
    model = Sequel
    template_naem = 'trblcms/sequel_detail.html'


def addOrEditSequel(request, pk=None):
    sequel = get_object_or_404(Sequel, id=pk, user=request.user) if pk else None
    form = SequelModelForm(instance=sequel)
    return render(request, 'trblcms/add_or_edit_sequel.html', {'sequel_form': form, 'pk': pk})


def saveOrUpdateSequel(request, pk=None):
    if request.method == 'POST':
        sequel, created = Sequel.objects.get_or_create(id=pk,
                user=request.user)
        form = SequelModelForm(request.POST, instance=sequel)
        if form.is_valid():
            sequel = form.save(commit=False)
            sequel.user = request.user
            sequel.save()

            # article slug or form slug
            return redirect(sequel.get_absolute_url())
        if created:
            sequel.delete()
        return redirect('trblcms:edit_sequel', pk=pk) # @!
    return redirect('main:home')


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
        else: print("form valid({}); content type({}) isn't matching".format(form.is_valid(), content_type))
    # @? comment redirection... where to go if fails?
    # @todo support many content type that inherits CommentedItemMixin
    return redirect(commented_item.get_absolute_url())


class SequelEditView(FormView):
    template_name = 'trblcms/sequel_edit.html'
    form_class = SequelModelForm
    # temp
    success_url = '/main/'

    #def form_valid(self, form):


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
