from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LicensePlateForm, UserProfileForm
from .models import LicensePlate
from garage.models import Booking

def register(request):
    initial_role = request.GET.get("role")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome to DalbaGo!")
            return redirect("core:dashboard")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.") 
    else:
        form = UserRegisterForm(initial={"role": initial_role})
    return render(request, "users/register.html", {"form": form})


def custom_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("core:landing")
    return render(request, "users/logout.html")

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("core:dashboard")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})

@login_required
def add_license_plate(request):
    if request.method == "POST":
        form = LicensePlateForm(request.POST)
        if form.is_valid():
            plate = form.save(commit=False)
            plate.user = request.user
            plate.save()
            return redirect("core:dashboard")
    else:
        form = LicensePlateForm()
    plates = request.user.plates.all()
    return render(request, "users/license_plates.html", {"form": form, "plates": plates})

@login_required
def profile(request):
    plates = request.user.plates.all()  # related_name="plates" on LicensePlate
    bookings = Booking.objects.filter(user=request.user).order_by("-start_time")
    return render(request, "users/profile.html", {
        "plates": plates,
        "bookings": bookings,
    })

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})

@login_required
def delete_license_plate(request, pk):
    plate = LicensePlate.objects.filter(pk=pk, user=request.user).first()
    if not plate:
        messages.error(request, "Plate not found or not yours.")
        return redirect("users:license_plates")

    if request.method == "POST":
        plate.delete()
        messages.success(request, "Plate deleted successfully.")
        return redirect("users:license_plates")

    return render(request, "users/confirm_delete_plate.html", {"plate": plate})
