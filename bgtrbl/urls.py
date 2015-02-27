from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from bgtrbl.main.views import profileView


urlpatterns = patterns('',
    url(r'^$', 'bgtrbl.main.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('bgtrbl.main.urls', namespace='main')),
    url(r'^trblcms/', include('bgtrbl.apps.trblcms.urls', namespace='trblcms')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', login_required(profileView), name='user_prfile'),
)
