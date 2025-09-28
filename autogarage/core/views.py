from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tools.models import Toolbox
from garage.models import AccessLog, Booking
from users.models import LicensePlate

def landing(request):
    return render(request, "landing.html")


@login_required
def dashboard(request):
    if request.user.garages.exists():
        return redirect("garage:owner_dashboard")
    else:
        return render(request, "dashboard_customer.html")
