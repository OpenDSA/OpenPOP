from django.conf.urls.defaults import *
from tastypie.api import Api
from visualize.api import StudentcodeResource

api = Api(api_name='v1')
api.register(StudentcodeResource())

urlpatterns = patterns('',
    (r'^', include(api.urls)),
)
