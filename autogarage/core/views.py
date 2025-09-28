from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tools.models import Toolbox
from garage.models import AccessLog, Booking
from users.models import LicensePlate

def landing(request):
    return render(request, "landing.html")

@login_required
def dashboard(request):
    if request.user.role == "owner":
        logs = AccessLog.objects.order_by("-timestamp")[:20]
        toolbox = Toolbox.objects.first()
        return render(request, "dashboard_owner.html", {"logs": logs, "toolbox": toolbox})
    else:
        bookings = Booking.objects.filter(user=request.user).order_by("-start_time")[:10]
        plates = LicensePlate.objects.filter(user=request.user)
        return render(request, "dashboard_customer.html", {"bookings": bookings, "plates":plates})
