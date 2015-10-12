from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=150 )
    name = models.CharField(max_length=250)
    department = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.code

    
class DegreePlan(models.Model):
    name = models.CharField(max_length = 250)
    owner = models.ForeignKey(User)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(self.owner))
        super(DegreePlan, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
  


class Class(models.Model):
    QUARTERS =(
              ("Autumn", 'Autumn'),
              ("Winter", "Winter"),
              ("Spring", "Spring")
              )
    course = models.ForeignKey(Course)
    plan= models.ForeignKey(DegreePlan)
    year = models.IntegerField()
    quarter = models.CharField(max_length=50, choices=QUARTERS)
    taken = models.BooleanField(default = False)
    
    
    def __unicode__(self):
        return self.course.code