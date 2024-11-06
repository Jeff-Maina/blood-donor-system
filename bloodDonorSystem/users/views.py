from django.shortcuts import render, redirect
from .form import RegisterUserForm, UserProfileForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home_view(request):
    return render(request, 'home.html')


def get_started(request):
    return render(request, 'get-started.html')


def login_user(request):
    return render(request, 'login.html')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = CustomUser.objects.create_user(
                email=email, password=password
            )

            login(request, user)
            return redirect("complete-profile")
    else:
        form = RegisterUserForm()
    return render(request, "user/register.html", {'form': form})


def complete_profile(request):
    if request.method == "POST":

        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.save()
            return redirect("dashboard")
    else:
        form = UserProfileForm()
    return render(request, "user/complete-profile.html", {"form": form})


def dashboard(request):
    return render(request, 'user/dashboard')
