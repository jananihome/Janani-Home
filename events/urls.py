from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view_events/$', views.view_events, name='view_events'),

   # url(r'^events/images$', views.view_images, name='images'),
]
