import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from users.models import LicensePlate
from garage.models import Booking, AccessLog
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PlateTestImage
from .utils import detect_plate_from_image
from django import forms


@csrf_exempt
def plate_check(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        payload = json.loads(request.body.decode("utf-8"))
        plate = payload.get("plate")
        plate = plate.replace(" ", "").upper()
        garage_id = payload.get("garage_id")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    try:
        lp = LicensePlate.objects.get(plate_number=plate)
    except LicensePlate.DoesNotExist:
        return JsonResponse({"access": False, "reason": "Unknown plate"}, status=403)

    # Find active booking for this user in this garage
    active_booking = Booking.objects.filter(
        user=lp.user, garage_id=garage_id, is_active=True
    ).first()

    if not active_booking:
        return JsonResponse({"access": False, "reason": "No active booking"}, status=403)

    # Log access
    AccessLog.objects.create(
        booking=active_booking,
        plate_detected=plate,
        timestamp=timezone.now(),
        door_opened=True,
    )

    return JsonResponse({
        "access": True,
        "user": lp.user.username,
        "garage": garage_id
    })


class PlateUploadForm(forms.ModelForm):
    class Meta:
        model = PlateTestImage
        fields = ["image"]

def upload_plate_image(request):
    if request.method == "POST":
        form = PlateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            plate = detect_plate_from_image(obj.image.path)
            if plate:
                plate = plate.replace(" ", "").upper()
            obj.detected_plate = plate
            obj.save()
            return render(request, "vision/plate_result.html", {"obj": obj, "plate": plate})
    else:
        form = PlateUploadForm()
    return render(request, "vision/plate_upload.html", {"form": form})