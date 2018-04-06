from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.announcement_list, name="announcement_list"),
]
