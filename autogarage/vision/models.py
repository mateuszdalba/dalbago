from django.db import models
from django.utils import timezone

class CleanlinessCheck(models.Model):
    booking = models.ForeignKey("garage.Booking", on_delete=models.CASCADE)
    before_image = models.ImageField(upload_to="cleanliness/before/")
    after_image = models.ImageField(upload_to="cleanliness/after/")
    passed = models.BooleanField(default=False)
    checked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cleanliness for {self.booking}"


class PlateTestImage(models.Model):
    image = models.ImageField(upload_to="plates/")
    detected_plate = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PlateTestImage {self.id} - {self.detected_plate or 'pending'}"