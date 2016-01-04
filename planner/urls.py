from django.conf.urls import include, url
from planner import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manager/', views.manager, name='manager'),
    url(r'^add/', views.add_plan, name='add'),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/$', views.viewplan, name="plan"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/$', views.delete, name="delete"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/(?P<_class>[\w\- ]+)/$', views.deleteclass, name="deleteclass"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/search/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/$', views.search_new, name="searchclass"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/search/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/(?P<search>[\w\- ]+)', views.search, name="searchclass"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/add/(?P<year>[\w\- ]+)/(?P<quarter>[\w\- ]+)/(?P<courseid>[\w\- ]+)', views.add_class, name="searchclass"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/delete/(?P<_class>[\w\- ]+)/$', views.deleteclass, name="test"),
    url(r'^plans/(?P<plan_slug>[\w\-]+)/removedmajor/(?P<majorid>[\w\-]+)/$', views.deletedmajor, name="delete declared major")
    
]
