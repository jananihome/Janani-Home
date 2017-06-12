from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.list_view, name='list_view'),
	url(r'^add-educational-need/$', views.add_educational_need, name='add_educational_need'),
]
