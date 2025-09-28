from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User
import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

class GarageAllowedActivity(models.Model):
    name = models.CharField(max_length=120)
    icon = models.CharField(max_length=50, blank=True, null=True)  # np. "fa-tools"

    def __str__(self):
        return self.name
    
class GarageForbiddenActivity(models.Model):
    name = models.CharField(max_length=120)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
class GarageTool(models.Model):
    name = models.CharField(max_length=120)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Garage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="garages")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="garages/", blank=True, null=True) # główne zdjęcie garażu
    is_available = models.BooleanField(default=True)

    allowed_activities = models.ManyToManyField(GarageAllowedActivity, blank=True, related_name="garages")
    forbidden_activities = models.ManyToManyField(GarageForbiddenActivity, blank=True, related_name="garages")
    tools = models.ManyToManyField(GarageTool, blank=True, related_name="garages")

    def __str__(self):
        return self.name
    


class Booking(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)  # ✅ new field
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancel_reason = models.CharField(max_length=255, blank=True, null=True)

    def is_active(self):
        now = timezone.now()
        return (
            not self.cancelled
            and self.start_time <= now <= self.end_time
        )

    def __str__(self):
        return f"{self.user.username} booking {self.garage.name}"

class AccessLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    plate_detected = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)
    door_opened = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plate_detected} at {self.timestamp}"

class Camera(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cameras")
    name = models.CharField(max_length=120)
    stream_url = models.CharField(max_length=500)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    # ✅ helpers for template
    def is_mjpeg(self):
        return self.stream_url and (".mjpg" in self.stream_url or "mjpeg" in self.stream_url)

    def is_http(self):
        return self.stream_url and self.stream_url.startswith("http")




@receiver(pre_save, sender=Garage)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, no old image to delete

    try:
        old_image = Garage.objects.get(pk=instance.pk).image
    except Garage.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=Garage)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)