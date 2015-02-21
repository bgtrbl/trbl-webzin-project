from django.conf.urls import patterns, include, url
from .views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bgtrbl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', home, name='home'),
)
