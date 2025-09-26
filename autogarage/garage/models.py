from django.db import models
from django.conf import settings
from django.utils import timezone

class Garage(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.garage} ({self.start_time})"

class AccessLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    plate_detected = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)
    door_opened = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plate_detected} at {self.timestamp}"
