from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.announcement_list, name="announcement_list"),
    url(r'^(?P<pk>\d+)/$', views.AnnouncementDetail.as_view(), name='announcement_detail'),    
]
