from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BookingForm, CameraForm
from django.shortcuts import get_object_or_404, redirect
from .models import Booking, Garage, Camera
from django.contrib import messages
from django.utils import timezone
import requests
from django.http import JsonResponse


@login_required
def owner_dashboard(request):
    # zakładamy że owner ma tylko jednen garage; dopasuj do twojej logiki
    garages = Garage.objects.filter(owner=request.user)
    cameras = Camera.objects.filter(owner=request.user)
    # Toolbox, logs etc. - pobierz jak masz
    return render(request, "dashboard_owner.html", {
        "garages": garages,
        "cameras": cameras,
        # "toolbox": toolbox, "logs": logs
    })

@login_required
def camera_add(request):
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            cam = form.save(commit=False)
            cam.owner = request.user
            cam.save()
            messages.success(request, "Camera saved.")
            return redirect("garage:owner_dashboard")
    else:
        form = CameraForm()
    return render(request, "garage/camera_form.html", {"form": form})

@login_required
def camera_edit(request, pk):
    cam = get_object_or_404(Camera, pk=pk, owner=request.user)
    if request.method == "POST":
        form = CameraForm(request.POST, instance=cam)
        if form.is_valid():
            form.save()
            messages.success(request, "Camera updated.")
            return redirect("garage:owner_dashboard")
    else:
        form = CameraForm(instance=cam)
    return render(request, "garage/camera_form.html", {"form": form, "camera": cam})

@login_required
def camera_delete(request, pk):
    cam = get_object_or_404(Camera, pk=pk, owner=request.user)
    if request.method == "POST":
        cam.delete()
        messages.success(request, "Camera removed.")
        return redirect("garage:owner_dashboard")
    return render(request, "garage/camera_confirm_delete.html", {"camera": cam})


# opcjonalnie: endpoint do walidacji URL (AJAX)
@login_required
def validate_camera_url(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"ok": False, "error": "No url"})
    try:
        r = requests.get(url, timeout=5)
        ok = r.status_code == 200
        return JsonResponse({"ok": ok, "status": r.status_code})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})



@login_required
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect("core:dashboard")
    else:
        form = BookingForm()
    return render(request, "garage/create_booking.html", {"form": form})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.cancelled:
        messages.warning(request, "This booking is already cancelled.")
        return redirect("users:profile")

    if request.method == "POST":
        reason = request.POST.get("reason", "")
        booking.cancelled = True
        booking.cancelled_at = timezone.now()
        booking.cancel_reason = reason
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("users:profile")

    return render(request, "garage/confirm_cancel_booking.html", {"booking": booking})