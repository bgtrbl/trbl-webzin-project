from django.conf.urls import patterns, url

from .views import formTest, ckeditorTest

urlpatterns = patterns('',
    url(r'^form_test/', formTest, name='form_test'),
    url(r'^ckeditor_test/', ckeditorTest, name = 'ckeditor_test'),
)
