from django.conf.urls import include, url
from planner import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manager/', views.manager, name='manager'),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/$', views.viewplan, name="plan"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/$', views.delete, name="delete"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/(?P<_class>[\w\- ]+)/$', views.deleteclass, name="deleteclass"),
    
    url(r'^plans/(?P<plan_slug>[\w\-]+)/add/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/(?P<courseid>[\w\- ]+)', views.add_class, name="searchclass"),
    
    #AJAX URLs for plan manager
    url(r'^removeplan/(?P<plan_id>[\w\-]+)', views.removeplan, name="removeplan"),
    url(r'^add/', views.add_plan, name='add'),
    #AJAX URLs for plan page
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/(?P<_class>[\w\- ]+)/$', views.deleteclass, name="test"),    
    url(r'^plans/(?P<plan_slug>[\w\-]+)/getdmajors/$', views.load_declared_majors),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/removedmajor/(?P<majorid>[\w\-]+)/$', views.deletedmajor, name="delete declared major"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/adddmajor/$',views.add_dmajor ),
    
    #AJAX search
    url(r'^plans/(?P<plan_slug>[\w\-]+)/search/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/query/$', views.search, name="searchpage"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/search/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/$', views.search_page, name="searchpage"),
    
]
