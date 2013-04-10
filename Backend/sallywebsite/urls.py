# Django
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
   (r'^api/', include('api_urls')),
   
)