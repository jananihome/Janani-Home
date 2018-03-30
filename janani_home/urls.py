from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^volunteers/', include('volunteers.urls')),
    url(r'', include('educational_need.urls')),
    url(r'', include('cms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
