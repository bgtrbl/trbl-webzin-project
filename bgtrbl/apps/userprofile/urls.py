from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import editUserProfile, updateUserProfile, myUserProfile,  UserProfileDetail


urlpatterns = patterns('',
    url(r'^update_profile/$', login_required(updateUserProfile), name='update_userprofile'),
    url(r'^edit_profile/$', login_required(editUserProfile), name='edit_userprofile'),
    url(r'^profile/$', login_required(myUserProfile), name='my_userprofile'),
    url(r'^profile/(?P<pk>[\d]+)/$', UserProfileDetail.as_view(), name='userprofile_detail'),
)
# temporary media url
