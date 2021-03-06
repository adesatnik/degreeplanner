from django import forms
from planner.models import *

def list_departments():
        list = []
        for course in Course.objects.all():
            if (course.department, course.department)  in list:
               break
                
            
            else:
                list.append((course.department, course.department))

                
        
        return list
    
class PlanForm(forms.ModelForm):
    class Meta:
        model = DegreePlan
        fields = ("name",)
QUARTERS =(
              ("Autumn", 'Autumn'),
              ("Winter", "Winter"),
              ("Spring", "Spring")
              )

class ClassForm(forms.Form):
    year = forms.IntegerField(required=True)
    quarter = forms.ChoiceField(choices=QUARTERS, required=True)
    taken = forms.BooleanField(required=False)


class DeptChoiceForm(forms.Form):
    depts = list_departments()
    department = forms.ChoiceField( choices = depts )

class SearchClassForm(forms.Form):
    searchterm = forms.CharField(required=False,label="Search " , max_length=10000)
    undergraduate = forms.BooleanField(required=False, label="Undergraduate" , initial=True)
    graduate = forms.BooleanField(required=False, label="Graduate")

class DeclareMajorForm(forms.Form):
    
    declared_major = forms.ModelChoiceField(queryset=Major.objects.all(), required=True)