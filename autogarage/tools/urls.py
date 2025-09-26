from django.urls import path
from . import views

app_name = "tools"

urlpatterns = [
    path("toolbox/<int:toolbox_id>/update/", views.update_toolbox_weight, name="update_toolbox_weight"),
    path("<int:pk>/update-reference/", views.update_reference, name="update_reference"),
]
