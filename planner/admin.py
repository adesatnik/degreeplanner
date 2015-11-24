from django.contrib import admin
from planner.models import Course, Class, DegreePlan, Quarter, Requirement
# Register your models here.

admin.site.register(Course)
admin.site.register(Class)
admin.site.register(DegreePlan)
admin.site.register(Quarter)
admin.site.register(Requirement)
