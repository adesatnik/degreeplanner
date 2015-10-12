from django.shortcuts import render
from planner.models import DegreePlan
from planner.forms import *
from django.http  import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def manager(request):
    plan_list = DegreePlan.objects.filter(owner=request.user)
    context = {"plans" : plan_list}
    return render(request, 'manager.html', context)

def viewplan(request, plan_slug ):
    plan = DegreePlan.objects.get(slug=plan_slug)
    context = {"plan" : plan}
    classset  = plan.class_set.all()
    
    authenticated = False
    if plan.owner == request.user:
        authenticated = True
    context['authenticated'] = authenticated
   
    if not classset: 
        notempty = False
    else:  
        notempty = True
    context['notempty'] = notempty
    
    classlist = []
    
    for i in range(1,5):   
        quarterlist = []
        set = plan.class_set.filter(year = i)
        for quarter in Class.QUARTERS:
            cquarter = quarter[0]
            quarterlist.append(set.filter(quarter=cquarter))
        classlist.append(quarterlist)
    context['classlist'] = classlist
    
    originals = []
    duplicates = []
    for course in classset:
        if course.course.code not in originals:
            originals.append(course.course.code)
        else:
            duplicates.append(course.course.code)
    print duplicates
    print originals
    if duplicates:
        duplicated = True
    else:
        duplicated = False 
    context['duplicated']= duplicated
    
    return render(request, 'plan.html', context)

def add_plan(request):
    context = {}
    if request.method == 'POST':
        form = PlanForm(data=request.POST)
        
        if form.is_valid():
            plan = form.save(commit=False)
            
            plan.owner=request.user
            plan.save()
        
        return HttpResponseRedirect('/planner/manager/')
        
    else:
        form = PlanForm()
    
    context["form"]= form   
    return render(request, "addplan.html", context)
    
def add_class(request, plan_slug, dept):
    context = {}
   
    if request.method== 'POST'   :
        form = ClassForm( data=request.POST, dep=dept)
        form.dept = dept
        if form.is_valid():
            current_class = form.save(commit= False)    
            
            current_class.plan = DegreePlan.objects.get(slug=plan_slug)
            current_class.save()
            
            return HttpResponseRedirect("/planner/plans/" + plan_slug) 
        
    else:
        form = ClassForm(dep=dept)
       
        
        
    
    context['form'] = form
   
    return render(request, "addclass.html", context)

def add_class_department(request, plan_slug):
    context = {}
    if request.method== 'POST':
        form = DeptChoiceForm(data=request.POST)
        if form.is_valid():
            dept = form.cleaned_data['department']
            deptstring = "".join(dept)
            
           
            
            return HttpResponseRedirect("/planner/plans/" + plan_slug + "/add/" + deptstring + "/")
    
    else:
        form = DeptChoiceForm()
    context['form'] = form
    return render(request, "deptchoice.html", context )
            
        
        