from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("profile/", views.profile, name="profile"),    
    path("profile/edit/", views.edit_profile, name="edit_profile"),# edit profile
    path("plates/", views.add_license_plate, name="license_plates"),
    path("plates/<int:pk>/delete/", views.delete_license_plate, name="delete_plate"),
]
