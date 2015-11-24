from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=150 )
    name = models.CharField(max_length=250)
    department = models.CharField(max_length=150)

    def __unicode__(self):
        return self.department + " " + self.code


class DegreePlan(models.Model):
    name = models.CharField(max_length = 250)
    owner = models.ForeignKey(User)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(self.owner))
        super(DegreePlan, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


QUARTERS =(
              ("Autumn", 'Autumn'),
              ("Winter", "Winter"),
              ("Spring", "Spring")
              )

class Class(models.Model):

    course = models.ForeignKey(Course)
    plan= models.ForeignKey(DegreePlan)
    year = models.IntegerField()
    quarter = models.CharField(max_length=50, choices=QUARTERS)
    taken = models.BooleanField(default = False)


    def __unicode__(self):
        return self.course.department + " " + self.course.code

class Quarter(models.Model):
    quarter = models.CharField(max_length=50, choices=QUARTERS)
    year = models.IntegerField()
    courses = models.ManyToManyField(Course)
    index = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.quarter == "Autumn":
            self.index = str(self.year) + "d"
        if self.quarter == "Winter":
            self.index =  str(self.year) + "a"
        if self.quarter == "Spring":
            self.index =  str(self.year) + "b"
        super(Quarter, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.quarter + " " + str(self.year)

class Requirement(models.Model):
    name = models.CharField(max_length=1000)
    number_required = models.IntegerField()
    classes = models.ManyToManyField(Course, blank=True)
    class_groups = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __unicode__(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=250)
    requirements = models.ManyToManyField(Requirement)

    def __unicode__(self):
        return self.name

