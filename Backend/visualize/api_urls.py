from django.conf.urls.defaults import *
from tastypie.api import Api

from visualize.api import StudentcodeResource

from visualize.api import ExerciseAssessResource

from visualize.api import ExercisewithJavaAssessResource

from visualize.api import ExerciseBTResource

api = Api(api_name='v1')
api.register(StudentcodeResource())
api.register(ExerciseAssessResource())
api.register(ExercisewithJavaAssessResource())
api.register(ExerciseBTResource())

urlpatterns = patterns('',
    (r'^', include(api.urls)),
)
