__author__ = 'Alejandro'

from bs4 import BeautifulSoup
from planner.models import Course
from django.core.management.base import BaseCommand, CommandError
import urllib2

def parse_program_of_study(url):
    coursestrings = []
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

    filtered = soup(class_="courseblocktitle")
    for f in filtered:
        coursestrings.append(f.get_text().split("."))

    for c in coursestrings:
        c[0] = c[0].encode("ascii", "replace").split("?")

    for c in coursestrings:
        if "-" not in c[0][1]:
            if not Course.objects.filter(code=c[0][1].strip(), name=c[1].strip(), department=c[0][0].strip()):
                c = Course(code=c[0][1].strip(), name=c[1].strip(), department=c[0][0].strip())
                c.save()




class Command(BaseCommand):
    help = 'Scrapes for classes'

    def add_arguments(self, parser):
        parser.add_argument("url", nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options["url"]:
            linkstrings = []
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, "lxml")

            for link in soup.find(id="/thecollege/programsofstudy/").children:
                if type(link.find("a")) != int:
                    linkurl = "http://collegecatalog.uchicago.edu" + link.find("a").get("href")
                    linkstrings.append(linkurl)

            for link in linkstrings:
                parse_program_of_study(link)

