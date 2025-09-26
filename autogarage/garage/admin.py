from django.contrib import admin
from .models import Garage, Booking, AccessLog

admin.site.register(Garage)
admin.site.register(Booking)
admin.site.register(AccessLog)
