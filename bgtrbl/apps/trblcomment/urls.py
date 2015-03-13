from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import saveComment, addComment


# @& ckeditor_upload loginrequired?
urlpatterns = patterns('',
    url(r'^save_comment/(?P<content_type>[\w]+)/(?P<pk>[\d]+)/$', login_required(saveComment), name = 'save_comment'),
    url(r'^add_comment/$', addComment, name = 'add_comment'),
)
