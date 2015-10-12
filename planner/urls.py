from django.conf.urls import include, url
from planner import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manager/', views.manager, name='manager'),
    url(r'^add/', views.add_plan, name='add'),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/$', views.viewplan, name="plan"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/add/$', views.add_class_department, name="addclassdepartment"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/add/(?P<dept>[\w\-]+)/$', views.add_class, name="plan"),
    
]
