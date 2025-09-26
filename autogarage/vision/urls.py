from django.urls import path
from . import views

app_name = "vision"

urlpatterns = [
    path("upload-plate/", views.upload_plate_image, name="upload_plate"),
]
