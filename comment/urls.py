from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^list/$', views.CommentListView.as_view(), name="comment_list"),
    url(r'^(?P<pk>\d+)/approve/$', views.comment_approval, name="comment_approval"),
    url(r'^(?P<pk>\d+)/activate/$', views.approve_comment, name="approve_comment"),
    url(r'^(?P<pk>\d+)/reject/$', views.reject_comment, name="reject_comment"),
    url(r'^educational_need/(?P<pk>\d+)/$', views.educational_need_comment, name='educational_need_comment'),
    url(r'^comment_submitted/$', views.comment_submitted, name='comment_submitted'),
]
