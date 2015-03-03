from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from bgtrbl.main.views import editUserProfile, updateUserProfile, myUserProfile,  UserProfileDetail

from .settings import MEDIA_ROOT


# @todo profile 관련 main 으로
urlpatterns = patterns('',
    url(r'^$', 'bgtrbl.main.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('bgtrbl.main.urls', namespace='main')),
    url(r'^trblcms/', include('bgtrbl.apps.trblcms.urls', namespace='trblcms')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/update_profile/$', login_required(updateUserProfile), name='update_userprofile'),
    url(r'^accounts/edit_profile/$', login_required(editUserProfile), name='edit_userprofile'),
    url(r'^accounts/profile/$', login_required(myUserProfile), name='my_userprofile'),
    url(r'^accounts/profile/(?P<pk>[\d]+)/$', UserProfileDetail.as_view(), name='userprofile_detail'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
# temporary media url
