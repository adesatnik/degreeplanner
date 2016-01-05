from django.shortcuts import render
from django.template.loader import render_to_string
from planner.models import *
from planner.forms import *
from django.http  import HttpResponseRedirect, JsonResponse
import time
# Create your views here.

def intersection(l1, l2):
    if l1 and l2:
        s2 = set(l2)
        return [val for val in l1 if val in s2 ]
    else:
        return []



def index(request):
    
    return render(request, 'index.html', {})

def manager(request):
    plan_list = DegreePlan.objects.filter(owner=request.user)
    context = {"plans" : plan_list}
    return render(request, 'manager.html', context)

QUARTERS =(
              ("Autumn", 'Autumn'),
              ("Winter", "Winter"),
              ("Spring", "Spring")
              )


def planmanager(request, plan_slug, template ):
    start = time.clock()
    plan = DegreePlan.objects.get(slug=plan_slug)
    
    form = DeclareMajorForm()
    context = {}
    context["form"] = form
    
    
    context["plan"] = plan
    declared_major_requirements = []
    for major in plan.declared_majors.all():
        declared_major_requirements.append((major.print_requirements(plan), major))
    context['declared_major_requirements'] = declared_major_requirements
    

    
    authenticated = False
    if plan.owner == request.user:
        authenticated = True
    context['authenticated'] = authenticated
    context['classlist'] = generate_classlist(plan)
    
    
    
    print time.clock() - start
    return render(request, template, context)

def generate_classlist(plan):

    classlist = []
    
    for i in range(1,5):   
        quarterlist = []
        set = plan.class_set.filter(year = i)
        for quarter in QUARTERS:
            cquarter = quarter[0]
            quarterlist.append(set.filter(quarter=cquarter))
        classlist.append(quarterlist)
        
    return classlist
    

def viewplan(request, plan_slug):
    return planmanager(request, plan_slug, "plan.html")

def delete(request, plan_slug):
    return planmanager(request, plan_slug, "plandelete.html")

def deleteclass(request,plan_slug, _class):
    plan = DegreePlan.objects.get(slug=plan_slug)
    if request.user == plan.owner:
        cl = Class.objects.get(id=_class)
        cl.delete()
        context = {'authenticated': True,
                   'classlist': generate_classlist(plan)}
        data = {'major_data' : generate_declared_majors(request, plan_slug),
                'plan_table' : render_to_string('plan_table.html', context)}
    return JsonResponse(data)

    

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
    
def add_class(request, plan_slug, year, quarter, courseid):
    context = {}
    course = Course.objects.get(id=courseid)
    plan = DegreePlan.objects.get(slug=plan_slug)
    quarter = int(quarter)
    quarter_string = ""
    if quarter == 1:
        quarter_string = "Autumn"
    elif quarter == 2:
        quarter_string = "Winter"
    elif quarter == 3:
        quarter_string = "Spring"
    new_class = Class(course=course, plan=plan, year=year, quarter=quarter_string)
    new_class.save()
    
    return HttpResponseRedirect("/planner/plans/" + plan_slug)
    




def search(request,plan_slug,year, quarter, search):
    context = {}
    if request.method == 'POST':
        form = SearchClassForm(data=request.POST)
        if form.is_valid():
            searchterm = form.cleaned_data["searchterm"]
            searchstring = "".join(searchterm)
            if form.cleaned_data["undergraduate"] and form.cleaned_data["graduate"]:
                level = "b"
            elif form.cleaned_data["undergraduate"]:
                level = "u"
            elif form.cleaned_data["graduate"]:
                level = "g"
            else:
                level = "n"
            if searchstring:
                return HttpResponseRedirect("/planner/plans/" + plan_slug + "/search/" + year + "/" + quarter + "/" + searchstring + level + "/")
            else:
                return HttpResponseRedirect("/planner/plans/" + plan_slug + "/search/" + year + "/" + quarter + "/")
    else:
        form = SearchClassForm()
        searchterms =[]
        level = search[-1:]
        search = search[:-1]

        for s in search.split(" "):
            searchterms.append(s)
        resultsn = list(Course.objects.all())
        resultsc = []
        results = []

        if search != "":
            for s in searchterms:


                try:
                    r = int(s)
                    resultsn = resultsn
                except:
                    resultsn = intersection(resultsn , list(Course.objects.filter(name__icontains=s))
                                            + list(Course.objects.filter(department__icontains=s)))

                resultsc = resultsc + list(Course.objects.filter(code__icontains=s))




        if search == "":
            results = []
        elif resultsc and resultsn:
            results = intersection(resultsc, resultsn)
        elif resultsc:
            results = resultsc
        elif resultsn:
            results = resultsn


        resultsf = []

        if level == "g":
            for r in results:
                if int(r.code) >= 30000:
                    resultsf.append(r)
        elif level == "u":
            for r in results:
                if int(r.code) < 30000:
                    resultsf.append(r)
        elif level == "b":
            resultsf = results

        resultsf = sorted(resultsf, key= lambda x: (x.department,x.code))
        context['year'] = year
        context['quarter'] = quarter
        context["results"] = resultsf


    context['form'] = form
    context["plan"] = DegreePlan.objects.get(slug=plan_slug)
    return render(request,"search.html", context)

def search_new(request,plan_slug, year, quarter):
    return search(request,plan_slug, year, quarter,"")

def add_dmajor(request, plan_slug):
    plan = DegreePlan.objects.get(slug=plan_slug)
    form = DeclareMajorForm(data=request.POST)
    if form.is_valid() and request.user == plan.owner:
        plan.declared_majors.add(form.cleaned_data["declared_major"])
        plan.save()
    
    data ={'major_data' : generate_declared_majors(request, plan_slug)}
    
    return JsonResponse(data)
            
def deletedmajor(request, plan_slug, majorid):
    major = Major.objects.get(id=majorid)
    plan = DegreePlan.objects.get(slug=plan_slug)
    if plan.owner == request.user:
        plan.declared_majors.remove(major)
    
    data ={'major_data' : generate_declared_majors(request, plan_slug)}
    
    return JsonResponse(data)
    
    

def load_declared_majors(request, plan_slug):
    data = {'major_data' : generate_declared_majors(request, plan_slug)}
    
    return JsonResponse(data)

def generate_declared_majors(request, plan_slug):
    context = {}
    plan = DegreePlan.objects.get(slug=plan_slug)
    context["plan"] = plan
    declared_major_requirements = []
    for major in plan.declared_majors.all():
        declared_major_requirements.append((major.print_requirements(plan), major))
    context['declared_major_requirements'] = declared_major_requirements
    if request.user == plan.owner:
        context['authenticated'] = True
    else:
        context['authenticated'] = False
    
    data = {}
    return render_to_string("declared_majors.html", context)
    
    
   







        
        