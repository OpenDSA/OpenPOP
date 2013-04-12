from django.db import models

# Create your models here.
class Studentcode(models.Model):
    id = models.BigIntegerField(default = 0)
    code = models.TextField()