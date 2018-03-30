from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.volunteer_list, name="volunteer_list"),
]
