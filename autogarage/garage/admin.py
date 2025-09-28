from django.contrib import admin
from .models import Garage, Booking, AccessLog

admin.site.register(Booking)
admin.site.register(AccessLog)

class GarageAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "location"]

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()

admin.site.register(Garage, GarageAdmin)