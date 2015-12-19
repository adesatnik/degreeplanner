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
                    if not cs:
                        print "Invalid class name"
                    else:
                        for c in cs:
                            requirement.classes.add(c)
                except:
                    "Invalid class name"
            if input == "x":
                dept = raw_input("Enter the department: ")
                filterstring = dept + " "
                n = int(raw_input("Enter the number of ranges: "))
                for i in range(0,n):
                    
                    range_input = raw_input("Enter the code lower bound \n " +
                                                "and code upper bound separated by a space in between and after: ")
                    filterstring = filterstring + range_input
                
                requirement.is_filter = True
                requirement.filter_string = filterstring
                requirement.filter_number_of_ranges = n
                requirement.save()
                active = False


            if input == "g":
                req_name = raw_input("Enter the requirement name: ")
                try:
                    requirement.class_groups.add(Requirement.objects.get(name=req_name))
                except:
                    print "Requirement name invalid"
        
        hidden = raw_input("Hidden? (Y/N)")
        if hidden == "Y":
            requirement.hidden = True
        else:
            print "Requirement not hidden"






















