from django.conf.urls import url, include
from django.contrib import admin
# Static helper function only for development!
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'', include('educational_need.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'session_security/', include('session_security.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
