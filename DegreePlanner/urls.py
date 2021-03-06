from django.conf.urls import include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.conf.urls.static import static
from DegreePlanner import settings
from pages import views



# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/planner/'

urlpatterns = [
    url(r'^$', views.index),           
    url(r'^work/', views.work),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^planner/', include('planner.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)