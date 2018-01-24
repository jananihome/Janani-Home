from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^edit_profile/$', views.update_profile, name='update_profile'),
    url(r'^edit_ngo_profile/$', views.update_ngo_profile, name='update_ngo_profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^ngo_signup/$', views.organization_signup, name='organization_signup'),
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': 'login'}),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activate_ngo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_organization, name='activate_organization'),
    url(r'^confirm_new_email/(?P<uidb64>[0-9A-Za-z_\-]+)/$',
        views.confirm_new_email, name='confirm_new_email'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^country/states/$', views.StateAjaxView, name='states_of_country'),
    url(r'^ngo_approval/(?P<pk>\d+)/$', views.ngo_approval, name="ngo_approval"),
    url(r'^(?P<pk>\d+)/ngo_approve/$', views.approve_ngo, name="approve_ngo"),
    url(r'^(?P<pk>\d+)/ngo_reject/$', views.reject_ngo, name="reject_ngo"),
]
