from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ("owner", "Garage Owner"),
        ("customer", "Garage User"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    
class LicensePlate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plates")
    plate_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.plate_number} ({self.user.username})"
