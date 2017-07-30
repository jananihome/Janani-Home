from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EducationalNeedListView.as_view(), name='list_view'),
    url(r'^educational_need/(?P<pk>\d+)/$', views.detail_view, name='detail_view'),
    url(r'^add-educational-need/$', views.add_need, name='add_need'),
    url(r'^educational-need/(?P<pk>\d+)/edit/$', views.edit_need, name='edit_need'),
    url(r'^educational-need/(?P<pk>\d+)/delete/$', views.delete_need, name='delete_need'),
    url(r'^educational-need/(?P<pk>\d+)/activate/$', views.activate_need, name='activate_need'),
    url(r'^educational-need/(?P<pk>\d+)/deactivate/$', views.deactivate_need, name='deactivate_need'),
    url(r'^educational_need/message_sent/$', views.message_sent, name='message_sent'),
]
