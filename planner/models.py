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





QUARTERS =(
              ("Autumn", 'Autumn'),
              ("Winter", "Winter"),
              ("Spring", "Spring")
              )



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
    
    def count_required(self):
        counter = 0
        if self.is_filter:
            counter = self.number_required
        
        for c in self.classes.all():
            counter = counter + 1
        
        for g in self.class_groups.all():
            g.count_required = childcount
            if not g.hidden:
                counter = counter + childcount
        
        return counter
            
    
    def meets_requirement(self, plan, acc= None, height = 0, course_set =[], used_courses = None):
        if acc is None:
            acc = []
        if used_courses is None:
            used_courses = []
            
        counter = 0

        if height == 0:
            class_set = plan.class_set.all()
            for c in class_set:
                course_set.append(c.course)        
        
        if self.class_groups.all():
            orderedreqs = []
            filterreqs = []
            for c in self.class_groups.all():
                if c.is_filter:
                    filterreqs.append(c)
                else:
                    orderedreqs.append(c)
            orderedreqs = orderedreqs + filterreqs            
            for r in orderedreqs:
                
                if r.hidden:
                    childrequirement = r.meets_requirement(plan, acc, height, course_set, used_courses )
                    if childrequirement[0][-1][1] == "satisfied":
                        counter = 1 + counter
                    used_courses = list(set(used_courses) | set(childrequirement[1]))

                else:
                    childrequirement = r.meets_requirement(plan, acc, height + 1, course_set, used_courses )
                    if childrequirement[0][-1][1] == "satisfied":
                        counter = 1 + counter
                    used_courses = list(set(used_courses) | set(childrequirement[1]))

                        
        if self.classes.all():
            for c in self.classes.all():
                if c in course_set and c not in used_courses:
                    counter = 1 + counter
                    if not self.hidden:
                        used_courses.append(c)
                else:
                    for crl in c.cross_listings.all():
                        if crl in course_set and c not in used_courses:
                            if not self.hidden:
                                used_courses.append(c)
                            counter = 1 + counter           
                            break
        if self.is_filter:
            filterdept = self.filter_string.split(" ")[0]
            coursenumbers = generate_filter_numbers(self)
            for c in course_set:
                if c.department == filterdept:
                    if int(c.code) in coursenumbers and c not in used_courses:
                        if not self.hidden:
                            used_courses.append(c)
                        counter = counter + 1    
                else:
                    for crl in c.cross_listings.all():
                        if crl.department == filterdept:
                            if int(crl.code) in coursenumbers and c not in used_courses:
                                if not self.hidden:
                                    used_courses.append(c)
                                counter = counter + 1
                                break

        if counter >= self.number_required:
            acc.append((self, "satisfied", height))
        else:
            acc.append((self, "not satisfied", height))
        
        return (acc, used_courses)
    
    

    
        


class Major(models.Model):
    name = models.CharField(max_length=250)
    requirements = models.OneToOneField(Requirement)
    notes = models.CharField(max_length=2000, blank=True)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super(Major, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
    def print_requirements(self, plan):
        unfiltered = reversed(self.requirements.meets_requirement(plan, [], 0, [])[0])
        ordered = order_requirements(list(unfiltered))
        filtered = []
        class_set = plan.class_set.all()
        course_set = []
        for c in class_set:
            course_set.append(c.course)
            for crl in c.course.cross_listings.all():
                course_set.append(crl)
        for group in ordered:
            filtered_group = []
            for k, v, h in group:
                req = k
                inplan = False
                classes = req.classes.all()
                classnames = []
                for c in classes:
                    inplan = False
                    if c in course_set:
                        inplan = True
                        course_set.remove(c)
                    classnames.append((c.department + " " + c.code, inplan))
                if req.filter_display:
                    filterclassnames = []
                    filter_string = req.filter_string.split(" ")
                    filterdept = filter_string[0]
                    filter_string.pop(0)       
                    coursenumbers = generate_filter_numbers(req)                        
                    for i in range(0,req.number_required): 
                        inplan = False
                        for c in course_set:
                            if c.department == filterdept and int(c.code) in coursenumbers:
                                course_set.remove(c)
                                inplan = True
                                break                             
                        filterclassnames.append((req.filter_display, inplan))
                    classnames = filterclassnames + classnames
                          
                if not req.hidden:
                    filtered_group.append((req, v, h, classnames))
            filtered.append(filtered_group)
        return filtered
    
def generate_filter_numbers(req):
    filter_string = req.filter_string.split(" ")
    filterdept = filter_string[0]
    filter_string.pop(0)
    coursenumbers = []
    blacklist_numbers = []
    for i in req.filter_blacklist.all():
        blacklist_numbers.append(int(i.code))
    for i in range(0,req.filter_number_of_ranges*2):
        if i % 2 !=0:
            pass
        else:
            for j in range(int(filter_string[i]), int(filter_string[i+1]) + 1):
                if j not in blacklist_numbers:
                    coursenumbers.append(j)     
    return coursenumbers     

def group_requirements(req_list):
    acc =[]
    grouped_list = []
    n = 0
    for r in req_list:
        n = n + 1
        if n == 1:
            grouped_list.append([r])
        elif n == len(req_list) :
            if r[2] == 1:
                grouped_list.append(acc)
                acc = []
                acc.append(r)
                grouped_list.append(acc)
            else:
                acc.append(r)
                grouped_list.append(acc)
        elif r[2] == 0:
            pass
        elif r[2] != 1:
            acc.append(r)
        else:
            grouped_list.append(acc)
            acc = []
            acc.append(r)

    grouped_list = list(reversed(grouped_list))
    grouped_list.insert(0, grouped_list[-1])
    grouped_list.pop(-1)
    grouped_list.pop(-1)
    return grouped_list

def order_requirements(req_list):
    grouped_list = group_requirements(req_list)
    ordered_list = []
    filters = []
    n = 0
    for r in grouped_list:
        if n == 0:
            ordered_list.append(r)
        else: 
            if r[0][0].is_filter:
                filters.append(r)
            else: 
                ordered_list.append(r)
        n = n +1
    ordered_list = ordered_list + filters

    return ordered_list
    
    
class DegreePlan(models.Model):
    name = models.CharField(max_length = 250)
    owner = models.ForeignKey(User)
    slug = models.SlugField(unique = True)
    declared_majors = models.ManyToManyField(Major, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(self.owner))
        super(DegreePlan, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Class(models.Model):

    course = models.ForeignKey(Course)
    plan= models.ForeignKey(DegreePlan)
    year = models.IntegerField()
    quarter = models.CharField(max_length=50, choices=QUARTERS)
    taken = models.BooleanField(default = False)


    def __unicode__(self):
        return self.course.department + " " + self.course.code
            
            
    


        

