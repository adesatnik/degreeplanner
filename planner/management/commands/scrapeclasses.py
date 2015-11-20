__author__ = 'Alejandro'
from bs4 import BeautifulSoup
from planner.models import Course, Quarter
from django.core.management.base import BaseCommand, CommandError
import urllib2

def parse_department_page(url, q):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    classes = []

    rows =soup(class_="resultrow")

    for row in rows:
        classes.append([
            row.find(class_="name").a.next_sibling.strip(),
            row.find(class_="two").string.strip()
        ])

    for cl in classes:
        if not Course.objects.filter(name=cl[1], department=(cl[0].split(" "))[0],
                   code=(((cl[0].split(" "))[1]).split("/"))[0]):
            c = Course(name=cl[1], department=(cl[0].split(" "))[0],
                       code=(((cl[0].split(" "))[1]).split("/"))[0]  )
            c.save()
            q.courses.add(c)







class Command(BaseCommand):
    help = "Scrapes the time schedules for classes"

    def add_arguments(self, parser):
        parser.add_argument("url", nargs='+', type=str)
        parser.add_argument("quarter", nargs="+" ,type=str)
        parser.add_argument("quarter", nargs="+", type=str)

    def handle(self, *args, **options):
        for url in options["url"]:
            linkstrings = []
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, "lxml")
            q = Quarter.objects.get(quarter = options["quarter"], year = options["year"])

            filtered = soup.find(id="tabs-1")
            filtered = filtered("li")

            for link in filtered:
                linkstrings.append("https://classes.uchicago.edu/" + link.find("a").get("href"))








