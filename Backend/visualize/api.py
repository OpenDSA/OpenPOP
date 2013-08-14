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


from ExerciseAssess import assess_code
from visualize.models import ExerciseAssess



from ExercisewithJavaAssess import withjavaassess
from visualize.models import ExercisewithJavaAssess

from ExerciseBT import btassess
from visualize.models import ExerciseBT

from LinkedListKAEx import assesskaex
from visualize.models import LinkedListKAEx

import jsonpickle, json


##########################################################################################################################
class LinkedListKAExResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset      = LinkedListKAEx.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'user/exercise'
        excludes      = []
        #object_class = ExerciseAssess
        serializer = Serializer(formats=['json'])
        #authentication  = Authentication()
        #authorization   = Authorization()
	
    def override_urls(self):
        return [
	   url(r"^(?P<resource_name>%s)/attempt%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('attempt'), name="api_assesskaex"),
	]
    
    def attempt(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):            
            returnedString= assesskaex(request.POST.get('code') , request.POST.get('genlist'))
            print returnedString
            #return self.create_response(request, {'streak':1 , 'progress': 2 , 'correct': False ,'feedback':returnedString[0] ,'details': returnedString[1] })
            return self.create_response(request, jsonpickle.encode({'streak':4 , 'progress': 2 , 'correct':returnedString[0]  ,'message':returnedString[1] , 'openPop': True  }))
        else :
             print "This is not an ajax call"
             return self.create_response(request, {'details': "Empty"})
        return  self.create_response(request, {}, HttpUnauthorized)


##########################################################################################################################
class ExerciseBTResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset = ExerciseBT.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'exercisebt'
        excludes = []
        #object_class = ExerciseAssess
        serializer = Serializer(formats=['json'])
        #authentication = Authentication()
        #authorization = Authorization()

    def override_urls(self):
        return [
url(r"^(?P<resource_name>%s)/btassessing%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('btassessing'), name="api_btassess"),
]
    
    def btassessing(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):
            print "api is called"
            returnedString= btassess(request.POST.get('code'))
            return self.create_response(request, {'data': returnedString})
        else :
             print "This is not an ajax call"
             return self.create_response(request, {'data': "Empty"})
        return self.create_response(request, {}, HttpUnauthorized)

############################################################################################################################################
class ExercisewithJavaAssessResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset = ExercisewithJavaAssess.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'exercisewithjavaassess'
        excludes = []
        #object_class = ExerciseAssess
        serializer = Serializer(formats=['json'])
        #authentication = Authentication()
        #authorization = Authorization()

    def override_urls(self):
        return [
url(r"^(?P<resource_name>%s)/javaassessing%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('javaassessing'), name="api_withjavaassess"),
]
    
    def javaassessing(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):
            print "api is called"
            returnedString= withjavaassess(request.POST.get('code'))
            return self.create_response(request, {'data': returnedString})
        else :
             print "This is not an ajax call"
             return self.create_response(request, {'data': "Empty"})
        return self.create_response(request, {}, HttpUnauthorized)


##############################################################################################################################################


class ExerciseAssessResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset      = ExerciseAssess.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'exerciseassess'
        excludes      = []
        #object_class = ExerciseAssess
        serializer = Serializer(formats=['json'])
        #authentication  = Authentication()
        #authorization   = Authorization()
	
    def override_urls(self):
        return [
	   url(r"^(?P<resource_name>%s)/startassessing%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('startassessing'), name="api_startassess"),
	]
    
    def startassessing(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):
            print "api is called"
            returnedString= assess_code(request.POST.get('code'))
            return self.create_response(request, {'data': returnedString})
        else :
             print "This is not an ajax call"
             return self.create_response(request, {'data': "Empty"})
        return  self.create_response(request, {}, HttpUnauthorized)

##############################################################################################################################################


class ExerciseAssessResource(ModelResource):
    def determine_format(self, request):
        return "application/json"
    def is_authenticated(self, request, **kwargs):
        return True
    def is_authorized(self, request, **kwargs):
        return True
    class Meta:
        queryset      = ExerciseAssess.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'exerciseassess'
        excludes      = []
        #object_class = ExerciseAssess
        serializer = Serializer(formats=['json'])
        #authentication  = Authentication()
        #authorization   = Authorization()
	
    def override_urls(self):
        return [
	   url(r"^(?P<resource_name>%s)/startassessing%s$" %(self._meta.resource_name, trailing_slash()),self.wrap_view('startassessing'), name="api_startassess"),
	]
    
    def startassessing(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.POST.get('code'):
            print "api is called"
            returnedString= assess_code(request.POST.get('code'))
            return self.create_response(request, {'data': returnedString})
        else :
             print "This is not an ajax call"
             return self.create_response(request, {'data': "Empty"})
        return  self.create_response(request, {}, HttpUnauthorized)



##############################################################################################################################################
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
             print "This is not an ajax call"
             return self.create_response(request, {'data': "Empty"})
        return  self.create_response(request, {}, HttpUnauthorized)

