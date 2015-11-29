from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=150 )
    name = models.CharField(max_length=250)
    department = models.CharField(max_length=150)
    cross_listings = models.ManyToManyField("self", )

    def __unicode__(self):
        return (self.department + " " + str(self.code))


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
    courses = models.ManyToManyField(Course, symmetrical=True, blank=True, default=None)
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
    name = models.CharField(max_length=1000, unique=True)
    number_required = models.IntegerField()
    classes = models.ManyToManyField(Course, blank=True)
    class_groups = models.ManyToManyField("self", blank=True, symmetrical=False)
    is_filter = models.BooleanField(default=False)
    filter_string = models.CharField(max_length=500, blank=True) #Must be of the form DEPT Lower_Bound Upper_Bound

    def __unicode__(self):
        return self.name

    def meets_requirement(self, plan):
        counter = 0
        if self.is_filter:
            filter_string = self.filter_string.split(" ")
            courses = Course.objects.filter(
                department=filter_string[0],
                code__range=(int(filter_string[1]), int(filter_string[2]))
            )
            for r in courses:
                for c in Class.objects.filter(course=r):
                    if c in plan.class_set.all():
                        counter = 1 + counter
                for crl in r.cross_listings.all():
                    for c in Class.objects.filter(course=crl):
                        if c in plan.class_set.all():
                            counter = 1 + counter


        else:
            if self.class_groups.all():
                for r in self.class_groups.all():
                    if r.meets_requirement(plan):
                        counter = 1 + counter
            if self.classes.all():
                for r in self.classes.all():
                    for c in Class.objects.filter(course=r):
                        if c in plan.class_set.all():
                            counter = 1 + counter
                    for crl in r.cross_listings.all():
                        for c in Class.objects.filter(course=crl):
                            if c in plan.class_set.all():
                                counter = 1 + counter

        if counter >= self.number_required:
            return True
        else:
            return False


class Major(models.Model):
    name = models.CharField(max_length=250)
    requirements = models.ManyToManyField(Requirement, blank=True)

    def __unicode__(self):
        return self.name

