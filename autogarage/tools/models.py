from django.db import models
from django.conf import settings
from django.utils import timezone


class Toolbox(models.Model):
    name = models.CharField(max_length=100, default="Main Toolbox")
    weight_ref = models.FloatField(help_text="Reference weight in grams")
    last_measured_weight = models.FloatField(default=0.0)
    last_check_ok = models.BooleanField(default=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} (ref: {self.weight_ref} g)"
