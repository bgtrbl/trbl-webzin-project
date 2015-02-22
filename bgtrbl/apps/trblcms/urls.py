from django.conf.urls import patterns, url

from .views import formTest, ckeditorTest, saveArticle, addOrEditArticle, Article

urlpatterns = patterns('',
    url(r'^save_article/$', saveArticle, name = 'save_article'),
    url(r'^add_or_edit_article/$', addOrEditArticle, name = 'add_article'),
    url(r'^add_or_edit_article/(?P<slug>[\w-]+)/$', addOrEditArticle, name = 'edit_article'),
    url(r'^form_test/', formTest, name='form_test'),
    url(r'^ckeditor_test/', ckeditorTest, name = 'ckeditor_test'),
)
