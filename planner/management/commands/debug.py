from django.core.management.base import BaseCommand, CommandError
from planner.models import *
from planner.views import *
class Command(BaseCommand):
    help = "Stuff happens"


    def handle(self, *args, **options):
        cs = Major.objects.get(name="Economics")
        plan = DegreePlan.objects.get(slug="econalex")
        cs.print_requirements(plan)
        
        