from django.db import models
from courses.models import Course
from coususers.models import CousUser

# Create your models here.

class Scrap(models.Model):
    course = models.ForeignKey(Course)
    cousUser = models.ForeignKey(CousUser)