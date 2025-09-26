from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm
from django.contrib import messages



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