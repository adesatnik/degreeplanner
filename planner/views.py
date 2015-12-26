from django.shortcuts import render
from planner.models import *
from planner.forms import *
from django.http  import HttpResponseRedirect
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
    major = Major.objects.get(name="Visual Arts")
    plan = DegreePlan.objects.get(slug=plan_slug)
    context = {"plan" : plan}
    classset  = plan.class_set.all()
    context['requirements'] = major.print_requirements(plan)

    
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
        for quarter in QUARTERS:
            cquarter = quarter[0]
            quarterlist.append(set.filter(quarter=cquarter))
        classlist.append(quarterlist)
    context['classlist'] = classlist
    
    
    
    
    return render(request, template, context)

def viewplan(request, plan_slug):
    return planmanager(request, plan_slug, "plan.html")

def delete(request, plan_slug):
    return planmanager(request, plan_slug, "plandelete.html")

def deleteclass(request,plan_slug, _class):
    cl = Class.objects.get(id=_class)
    cl.delete()
    
    return HttpResponse("")

    

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
    
def add_class(request, plan_slug, coursei):
    context = {}
   
    if request.method== 'POST':
        form = ClassForm(data=request.POST)
        assert form
        if form.is_valid():
            c = Class(course=Course.objects.get(code=coursei.split(" ")[1], department=coursei.split(" ")[0])
                      , plan = DegreePlan.objects.get(slug=plan_slug), year = form.cleaned_data["year"],
                      quarter = form.cleaned_data["quarter"], taken=form.cleaned_data["taken"])

            if not Class.objects.filter(course=Course.objects.get(code=coursei.split(" ")[1], department=coursei.split(" ")[0])
                      , plan = DegreePlan.objects.get(slug=plan_slug), year = form.cleaned_data["year"],
                      quarter = form.cleaned_data["quarter"], taken=form.cleaned_data["taken"]):
                c.save()


            return HttpResponseRedirect("/planner/plans/" + plan_slug)
        
    else:
        form = ClassForm()
        context["course"] = coursei
       
        
        
    
    context['form'] = form
   
    return render(request, "addclass.html", context)




def search(request,plan_slug,search):
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
                return HttpResponseRedirect("/planner/plans/" + plan_slug + "/search/" + searchstring + level + "/")
            else:
                return HttpResponseRedirect("/planner/plans/" + plan_slug + "/search/")
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

        context["results"] = resultsf


    context['form'] = form
    context["plan"] = DegreePlan.objects.get(slug=plan_slug)
    return render(request,"search.html", context)

def search_new(request,plan_slug):
    return search(request,plan_slug,"")









        
        