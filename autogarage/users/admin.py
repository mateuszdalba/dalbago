from django.contrib import admin
from .models import User, LicensePlate
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(LicensePlate)
class LicensePlateAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "user")
