from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from . import views

sitemaps = {
    'static_pages': views.StaticViewSitemap,
    'cms_pages': views.CmsSitemap,
    'educational_needs': views.EducationalNeedSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # Our apps
    url(r'^accounts/', include('accounts.urls')),
    url(r'^announcements/', include('announcements.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^volunteers/', include('volunteers.urls')),
    url(r'^events/', include('events.urls')),
    url(r'', include('educational_need.urls')),
    url(r'', include('cms.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    #import debug_toolbar
    #urlpatterns = [
    #    url(r'^__debug__/', include(debug_toolbar.urls)),
    #] + urlpatterns
