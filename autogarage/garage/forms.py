from django import forms
from .models import Booking
from .models import Camera
from .models import Garage
from django.core.exceptions import ValidationError

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
        exclude = ['owner'] 
        fields = ["name", "description", "price_per_hour", "location", "image",
                 "allowed_activities", "forbidden_activities", "tools"]
        widgets = {
            "allowed_activities": forms.CheckboxSelectMultiple,
            "forbidden_activities": forms.CheckboxSelectMultiple,
            "tools": forms.CheckboxSelectMultiple,
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPEG and PNG formats are allowed.")
            if image.size > 5 * 1024 * 1024:  # Optional: 5MB limit
                raise ValidationError("Image file too large (max 5MB).")
        return image