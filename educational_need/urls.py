from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.list_view, name='list_view'),
]
