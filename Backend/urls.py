# Django
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   (r'^api/', include('api_urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),)
