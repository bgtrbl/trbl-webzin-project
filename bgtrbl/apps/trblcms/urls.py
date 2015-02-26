from django.conf.urls import patterns, url

from .views import ckeditorTest, saveArticle, saveComment, addOrEditArticle, ArticleDetailView, ArticleListView

urlpatterns = patterns('',
    url(r'^articles/$', ArticleListView.as_view(), name = 'article_list'),
    url(r'^article/(?P<slug>[\w\_\-]+)/$', ArticleDetailView.as_view(), name = 'article_detail'),
    url(r'^save_article/$', saveArticle, name = 'save_article'),
    url(r'^save_comment/(?P<content_type>[\w]+)/(?P<pk>[\d]+)/$', saveComment, name = 'save_comment'),
    url(r'^add_or_edit_article/$', addOrEditArticle, name = 'add_article'),
    url(r'^add_or_edit_article/(?P<slug>[\w\_\-]+)/$', addOrEditArticle, name = 'edit_article'),
    url(r'^ckeditor_test/', ckeditorTest, name = 'ckeditor_test'),
)
