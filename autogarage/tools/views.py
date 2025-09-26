from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Toolbox
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ToolboxReferenceForm

@csrf_exempt  # allow external device to call without CSRF token
def update_toolbox_weight(request, toolbox_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        payload = json.loads(request.body.decode("utf-8"))
        current_weight = float(payload.get("weight"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or missing 'weight'")

    try:
        toolbox = Toolbox.objects.get(pk=toolbox_id)
    except Toolbox.DoesNotExist:
        return HttpResponseBadRequest("Toolbox not found")

    # update toolbox status
    toolbox.last_measured_weight = current_weight
    toolbox.last_check_ok = abs(current_weight - toolbox.weight_ref) < 50  # tolerance 50g
    toolbox.updated_at = timezone.now()
    toolbox.save()

    return JsonResponse({
        "toolbox": toolbox.name,
        "ref_weight": toolbox.weight_ref,
        "measured": current_weight,
        "ok": toolbox.last_check_ok,
        "updated_at": toolbox.updated_at,
    })

@require_POST
def update_reference(request, pk):
    toolbox = get_object_or_404(Toolbox, pk=pk)
    form = ToolboxReferenceForm(request.POST, instance=toolbox)
    if form.is_valid():
        form.save()
        messages.success(request, f"Toolbox reference weight updated to {toolbox.weight_ref} g.")
    else:
        messages.error(request, "Invalid input. Please try again.")
    return redirect("core:dashboard")