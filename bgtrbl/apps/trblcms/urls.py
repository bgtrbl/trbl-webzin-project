from django.conf.urls import patterns, url

from .views import formTest, ckeditorTest, saveArticle, addOrEditArticle, Article
from .views import ckeditorTest, saveArticle, addOrEditArticle, ArticleDetailView, ArticleListView

urlpatterns = patterns('',
    url(r'^article/$', ArticleListView.as_view(), name = 'article_list'),
    url(r'^article/(?P<slug>[\w\_\-]+)/$', ArticleDetailView.as_view(), name = 'article_detail'),
    url(r'^save_article/$', saveArticle, name = 'save_article'),
    url(r'^add_or_edit_article/$', addOrEditArticle, name = 'add_article'),
    url(r'^add_or_edit_article/(?P<slug>[\w\_\-]+)/$', addOrEditArticle, name = 'edit_article'),
    url(r'^ckeditor_test/', ckeditorTest, name = 'ckeditor_test'),
)
