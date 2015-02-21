from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^main/', include('bgtrbl.main.urls', namespace='main')),
    url(r'^trblcms/', include('bgtrbl.apps.trblcms.urls', namespace='trblcms')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
