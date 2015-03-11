from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import ArticleDetailView, addArticle, editArticle
from .views import SequelDetailView, addSequel, editSequel

# @goaway
from .views import SequelEditView, ArticleListView, ArticleDeleteView

from ckeditor.views import upload as ckeditor_upload


# @& ckeditor_upload loginrequired?
urlpatterns = patterns('',
    url(r'^ckeditor_upload/', ckeditor_upload, name='ckeditor_upload'),
    url(r'^article/(?P<slug>[\w\_\-]+)/$', ArticleDetailView.as_view(), name = 'article_detail'),
    url(r'^add_article/$', login_required(addArticle), name = 'add_article'),
    url(r'^edit_article/(?P<pk>[\d]+)/$', login_required(editArticle), name = 'edit_article'),
    url(r'^delete_article/(?P<pk>[\d]+)/$', login_required(ArticleDeleteView.as_view()), name = 'delete_article'),
    url(r'^sequel/(?P<slug>[\w\_\-]+)/$', SequelDetailView.as_view(), name= 'sequel_detail'),
    url(r'^add_sequel/$', login_required(addSequel), name = 'add_sequel'),
    url(r'^edit_sequel/(?P<pk>[\d]+)/$', login_required(editSequel), name = 'edit_sequel'),
    url(r'^articles/$', ArticleListView.as_view(), name = 'article_list'),
    url(r'^sequel_edit_test/(?P<slug>[\w\_\-]+)/$', SequelEditView.as_view(), name= 'sequel_edit'),
)
