from django import forms
from planner.models import DegreePlan, Class, Course

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
        
class ClassForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset = Course.objects.none())
    def __init__(self,*args,**kwargs):
        
        self.dep = kwargs.pop('dep')
       
        super(ClassForm,self).__init__(*args,**kwargs)
        qs = Course.objects.filter(department=self.dep)
        self.fields['course'].queryset = qs
       
     
        
   
    
    
    
    class Meta:
        model = Class
        fields =("course", "year", "quarter" , "taken")

class DeptChoiceForm(forms.Form):
    
    department = forms.ChoiceField( choices = list_departments() )