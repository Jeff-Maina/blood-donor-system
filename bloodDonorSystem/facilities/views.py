from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import RegisterFacilityForm
from users.models import CustomUser
from django.contrib.auth import authenticate, login, logout


# Create your views here.


@login_required
def dashboard_view(request):
    pass


def register_facility(request):
    if request.method == "POST":
        form = RegisterFacilityForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            facility_name = form.cleaned_data.get("facility_name")
            registration_number = form.cleaned_data.get("registration_number")

            user = CustomUser.objects.create_user(
                email=email, password=password, role='facility', facility_name=facility_name, registration_number=registration_number)

            login(request, user)

            return redirect("awaiting-approval")
    else:
        form = RegisterFacilityForm()
    return render(request, "facility/register.html", {'form': form})
