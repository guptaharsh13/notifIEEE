from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_title = "NOTIFIEEE"
admin.site.site_header = "NOTIFIEEE Admin Panel"
admin.site.index_title = "Welcome to NOTIFIEEE Admin Panel"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("slack/events/", include("events.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
