from django.conf.urls import patterns, url, include

from .views import home, allauthTest, profileView

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^allauth_test/', allauthTest, name='allauth_test'),
)
