from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import home, allauthTest, Magazine, Forum


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^allauth_test/', allauthTest, name='allauth_test'),
    url(r'^flatpage/(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage', name='flatpage'),
    url(r'^magazine/', Magazine.as_view(), name='magazine'),
    url(r'^forum/', Forum.as_view(), name='forum'),

)

# url(r'^pages/(?P<url>).*$', include('django.contrib.flatpages.urls')),
