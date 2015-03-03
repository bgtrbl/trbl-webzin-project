from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import SequelEditView, ArticleListView
from .views import ArticleDetailView, addOrEditArticle, saveOrUpdateArticle
from .views import SequelDetailView, addOrEditSequel, saveOrUpdateSequel
from .views import saveComment


urlpatterns = patterns('',
    url(r'^article/(?P<slug>[\w\_\-]+)/$', ArticleDetailView.as_view(), name = 'article_detail'),
    url(r'^add_article/$', login_required(addOrEditArticle), name = 'add_article'),
    url(r'^edit_article/(?P<pk>[\d]+)/$', login_required(addOrEditArticle), name = 'edit_article'),
    url(r'^save_article/$', login_required(saveOrUpdateArticle), name = 'save_article'),
    url(r'^update_article/(?P<pk>[\d]+)$', login_required(saveOrUpdateArticle), name = 'update_article'),
    url(r'^sequel/(?P<slug>[\w\_\-]+)/$', SequelDetailView.as_view(), name= 'sequel_detail'),
    url(r'^add_sequel/$', login_required(addOrEditSequel), name = 'add_sequel'),
    url(r'^edit_sequel/(?P<pk>[\d]+)/$', login_required(addOrEditSequel), name = 'edit_sequel'),
    url(r'^save_sequel/$', login_required(saveOrUpdateSequel), name = 'save_sequel'),
    url(r'^update_sequel/(?P<pk>[\d]+)$', login_required(saveOrUpdateSequel), name = 'update_sequel'),
    url(r'^save_comment/(?P<content_type>[\w]+)/(?P<pk>[\d]+)/$', login_required(saveComment), name = 'save_comment'),
    url(r'^articles/$', ArticleListView.as_view(), name = 'article_list'),
    url(r'^sequel_edit_test/(?P<slug>[\w\_\-]+)/$', SequelEditView.as_view(), name= 'sequel_edit'),
)
