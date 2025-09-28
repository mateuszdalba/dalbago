from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("vision/", include("vision.urls")),
    path("tools/", include("tools.urls")),
    path("garage/", include("garage.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)