from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("vision/", include("vision.urls")),
    path("tools/", include("tools.urls")),
]