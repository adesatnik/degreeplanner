__author__ = 'Alejandro'
from django.core.management.base import BaseCommand, CommandError
from planner.models import Major, Requirement, Course

class Command(BaseCommand):
    help = "adds a new requirement to the database"


    def handle(self, *args, **options):
        name = raw_input("Name? ")






        try:
            requirement = Requirement.objects.get(name=name)
            print "You are editing an existing requirement"
        except:
            number_required = raw_input("Number of sub-requirements? ")
            requirement = Requirement(name=name, number_required=number_required)
            requirement.save()

        active = True

        while active:
            input = raw_input("Enter c for class, x for group of classes, or g for a group, "
                              + " or q to finish: ")
            if input == "q":
                active =False
            if input == "c":
                class_name = raw_input("Enter the class name: ")
                try:
                    cs = Course.objects.filter(code=class_name.split(" ")[1], department=class_name.split(" ")[0])
                    for c in cs:
                        requirement.classes.add(c)
                except:
                    "Invalid class name"
            if input == "x":
                range_input = raw_input("Enter the department, the code lower bound \n " +
                                            "and code upper bound separated by spaces: ")
                requirement.is_filter = True
                requirement.filter_string = range_input
                requirement.save()
                active = False


            if input == "g":
                req_name = raw_input("Enter the requirement name: ")
                try:
                    requirement.class_groups.add(Requirement.objects.get(name=req_name))
                except:
                    print "Requirement name invalid"






        """if is_root == "y":
            active = True
            while active:
                class_name = raw_input("Enter the class name, enter x for a range of classes, or enter q if you are done: ")
                if class_name == "q":
                    active = False
                if class_name == "x":
                    range_input = raw_input("Enter the department, the code lower bound \n " +
                                            "and code upper bound separated by spaces: ")
                    class_range = Course.objects.filter(department=range_input.split(" ")[0],
                                                        code__range=(int(range_input.split(" ")[1]),
                                                                     int(range_input.split(" ")[2])) )
                    for c in class_range:
                        print c
                        classes.append(str(c))
                else:
                    if class_name != "q":
                        classes.append(class_name)

            req = Requirement(name=name, number_required=number_required)
            req.save()
            for c in classes:
                print c
                for cl in Course.objects.filter(code=c.split(" ")[1], department=c.split(" ")[0]):
                    req.classes.add(cl)
            req.save()

            print req.classes.all()

        elif (is_root == "n"):
            active = True
            reqs = []
            while active:
                req_name = raw_input("Enter the requirement name, or enter q if you are done: ")
                if req_name == "q":
                    active = False
                else:
                    if (Requirement.objects.get(name=req_name)):
                        reqs.append(req_name)
                    else: print "Requirement does not exist, try again. "

            req = Requirement(name=name, number_required=number_required)
            req.save()
            for r in reqs:
                req.class_groups.add(Requirement.objects.get(name=r))
            req.save()

            print req.class_groups.all()"""

















