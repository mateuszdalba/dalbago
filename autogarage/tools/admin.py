from django.contrib import admin
from .models import Toolbox

@admin.register(Toolbox)
class ToolboxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "weight_ref", "last_measured_weight", "last_check_ok", "updated_at")
