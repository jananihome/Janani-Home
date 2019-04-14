from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='dashboard', permanent=True), name='index'),
    url(r'^dashboard/$', views.dashboard, name="superadmin_dashboard"),
    url(r'^users/$', views.user_list, name="superadmin_user_list"),
]
