from django.urls import path
from . import views

app_name = "garage"

urlpatterns = [
    path("book/", views.create_booking, name="create_booking"),
    path("booking/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("camera/add/", views.camera_add, name="camera_add"),
    path("camera/<int:pk>/edit/", views.camera_edit, name="camera_edit"),
    path("camera/<int:pk>/delete/", views.camera_delete, name="camera_delete"),
    path("camera/validate/", views.validate_camera_url, name="camera_validate"),
]
