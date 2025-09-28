from django import forms
from .models import Booking
from .models import Camera
from .models import Garage

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["garage", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ["name", "stream_url", "username", "password", "is_active"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ["name", "description", "price_per_hour", "location", "features", "activities", "image"]
        widgets = {
            "features": forms.CheckboxSelectMultiple,
            "activities": forms.CheckboxSelectMultiple,
        }