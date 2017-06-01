from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.educational_need, name='educational_need'),
]
