# myapp/api.py
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.resources import ModelResource
# Tastypie
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest
from tastypie.models import ApiKey
from tastypie.exceptions import NotRegistered, BadRequest


from django.conf.urls.defaults import patterns, url
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.db import transaction, IntegrityError

from StudentCode import visualize_code
from visualize.models import Studentcode


class StudentcodeResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset      = Studentcode.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'studentcode'
        excludes      = []
        #object_class = Studentcode
        serializer = Serializer(formats=['json'])
        #authentication  = Authentication()
        #authorization   = Authorization()
	
    def override_urls(self):
        return [
	   url(r"^(?P<resource_name>%s)/startvisualizing%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('startvisualizing'), name="api_startvisual"),
	]
    
    def startvisualizing(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):
            print "api is called"
            returnedString= visualize_code(request.POST.get('code'))
            return self.create_response(request, {'data': returnedString})
        else :
             print "This is not un ajax call"
             return self.create_response(request, {'data': "Empty"})
        return  self.create_response(request, {}, HttpUnauthorized)

