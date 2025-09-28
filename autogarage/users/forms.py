from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LicensePlate

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "role",
            "password1",
            "password2",
        ]


class LicensePlateForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ["plate_number"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "address"]