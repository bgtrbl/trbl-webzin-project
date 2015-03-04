from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from bgtrbl.apps.userprofile.views import editUserProfile, updateUserProfile, myUserProfile,  UserProfileDetail

from .settings import MEDIA_ROOT


# @todo profile 관련 main 으로
urlpatterns = patterns('',
    url(r'^$', 'bgtrbl.main.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('bgtrbl.main.urls', namespace='main')),
    url(r'^trblcms/', include('bgtrbl.apps.trblcms.urls', namespace='trblcms')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^userprofile/', include('bgtrbl.apps.userprofile.urls', namespace='userprofile')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
# temporary media url
