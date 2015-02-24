from django.conf.urls import patterns, url

from .views import home, allauthTest, profileView

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^allauth_test/', allauthTest, name='allauth_test'),
    url(r'^(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage', name='flatpage'),
)

# url(r'^pages/(?P<url>).*$', include('django.contrib.flatpages.urls')),
