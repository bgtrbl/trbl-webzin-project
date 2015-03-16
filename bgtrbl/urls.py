from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from django.views.generic.base import RedirectView
from django.http import HttpResponse

from bgtrbl.apps.userprofile.views import editUserProfile, updateUserProfile, myUserProfile,  UserProfileDetail

# @todo fix this
from .settings import MEDIA_ROOT


# @todo profile 관련 main 으로
urlpatterns = patterns('',
    url(r'^$', 'bgtrbl.main.views.home', name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('bgtrbl.main.urls', namespace='main')),
    url(r'^trblcms/', include('bgtrbl.apps.trblcms.urls', namespace='trblcms')),
    url(r'^trblcomment/', include('bgtrbl.apps.trblcomment.urls', namespace='trblcomment')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^userprofile/', include('bgtrbl.apps.userprofile.urls', namespace='userprofile')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    url(r'^flatpage/(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage', name='flatpage'),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
)
# temporary media url 나중에 지워야함
