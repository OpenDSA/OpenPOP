from django.db import models

# Create your models here.
class Studentcode(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()

class ExerciseAssess(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()


class ExercisewithJavaAssess(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()

class ExerciseBT(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()

class LinkedListKAEx(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()
