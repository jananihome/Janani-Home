from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.VolunteerList.as_view(), name="volunteer_list"),
]
