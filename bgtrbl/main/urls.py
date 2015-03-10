from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import home, allauthTest, forum, magazine


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^allauth_test/', allauthTest, name='allauth_test'),
    url(r'^magazine/', magazine, name='magazine'),
    url(r'^forum/', forum, name='forum'),

)

# url(r'^pages/(?P<url>).*$', include('django.contrib.flatpages.urls')),
