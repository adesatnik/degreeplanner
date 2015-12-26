from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import collections


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
    #settings for filters
    is_filter = models.BooleanField(default=False)
    filter_string = models.CharField(max_length=500, blank=True) #Must be of the form DEPT Lower_Bound Upper_Bound
    filter_number_of_ranges = models.IntegerField(blank=True, default=0)
    hidden = models.BooleanField(default=False)
    filter_display = models.CharField(max_length=100, blank=True)
    filter_blacklist = models.ManyToManyField(Course, blank = True, related_name="requirement_filter_blacklist")


    def __unicode__(self):
        return self.name
    
    def meets_requirement(self, plan, acc= [], height = 0):
        counter = 0
        
        if self.is_filter:
            filter_string = self.filter_string.split(" ")
            filterdept = filter_string[0]
            filter_string.pop(0)
            courses = Course.objects.none()
            for i in range(0,self.filter_number_of_ranges*2):
                if i % 2 !=0:
                    pass
                else:
                    courses = courses | Course.objects.filter(
                        department=filterdept,
                        code__range=(int(filter_string[i]), int(filter_string[i+1]))
                    )
            print courses
            courses = courses.exclude(id__in=self.filter_blacklist.all())
            print courses
            for r in courses:
                for c in Class.objects.filter(course=r):
                    if c in plan.class_set.all():
                        counter = 1 + counter
                    else:
                        for crl in r.cross_listings.all():
                            for c in Class.objects.filter(course=crl):
                                if c in plan.class_set.all():
                                    counter = 1 + counter
                                    break
        if self.class_groups.all():
            for r in self.class_groups.all():
                if r.hidden:
                    if r.meets_requirement(plan, acc, height)[0][1] == "satisfied":
                        counter = 1 + counter
                else:
                    if r.meets_requirement(plan, acc, height + 1)[0][1] == "not satisfied":
                        pass
        if self.classes.all():
            for r in self.classes.all():
                for c in Class.objects.filter(course=r):
                    if c in plan.class_set.all():
                        counter = 1 + counter
                else:
                    for crl in r.cross_listings.all():
                        for c in Class.objects.filter(course=crl):
                            if c in plan.class_set.all():
                                counter = 1 + counter
                                break

        if counter >= self.number_required:
            acc.append((self.name, "satisfied", height))
        else:
            acc.append((self.name, "not satisfied", height))
        
        return acc
    
    

    
        


class Major(models.Model):
    name = models.CharField(max_length=250)
    requirements = models.OneToOneField(Requirement)
    notes = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.name
    
    def print_requirements(self, plan):
        unfiltered = reversed(self.requirements.meets_requirement(plan, []))
        filtered = []
        for k, v, h in unfiltered:
            req = Requirement.objects.get(name=k)
            classes = req.classes.all()
            classnames = []
            if req.filter_display:
                for i in range(0,req.number_required):
                    classnames.append(req.filter_display)
            for c in classes:
                classnames.append(c.department + " " + c.code)
                
            if not req.hidden:
                filtered.append((req.name, v, h, classnames))
                
        return filtered
    
    
        

    

