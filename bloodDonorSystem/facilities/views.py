from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import RegisterFacilityForm, ProfileFacilityForm
from users.models import CustomUser, Request, Donation
from .models import FacilityProfile
from django.contrib.auth import authenticate, login, logout
from .decorators import facility_required

# Create your views here.


@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser:
        return redirect('admin:index')

    if user.role == 'facility':
        if user.is_approved:
            if user.profile_completed:
                profile = user.facilityprofile
                donations = profile.donations.all()
                total_donations = donations.count()
                requests = profile.requests.all()

                pending_requests_count = requests.filter(
                    approval_status='pending').count()
                total_requests = requests.count()

                completed_donations = donations.filter(
                    status='completed',
                )

                total_blood_donated = sum(
                    donation.amount for donation in completed_donations)

                context = {
                    'user': user,
                    'profile': profile,
                    'donations': donations,
                    'total_donations': total_donations,
                    'pending_requests_count': pending_requests_count,
                    'total_requests': total_requests,
                    'total_blood_donated': total_blood_donated/1000

                }

                return render(request, 'facility/dashboard.html', context)
            else:
                return redirect("complete-facility-profile")
        else:
            return redirect('awaiting-approval')
    else:
        return redirect('user-dashboard')


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


@login_required
def awaiting_approval(request):
    user = request.user
    if user.role == 'facility':
        if user.is_approved:
            return redirect("facility-dashboard")
        else:
            return render(request, "facility/awaiting-approval.html", {'email': user.email})
    else:
        return redirect('user-dashboard')


@login_required
def complete_profile(request):
    try:
        facility_profile = FacilityProfile.objects.get(user=request.user)
    except FacilityProfile.DoesNotExist:
        facility_profile = None

    # if request.user.profile_completed:
    #     return redirect('facility-dashboard')

    if request.method == 'POST':
        print("hello world")
        form = ProfileFacilityForm(request.POST, instance=facility_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile = form.complete_profile()

            if profile:
                return redirect("facility-dashboard")
            else:
                print(form.errors)
        else:
            print(form.errors)
    else:
        form = ProfileFacilityForm(instance=facility_profile)

    return render(request, "facility/complete-profile.html", {'form': form, 'error': form.errors})


# ! REQUESTS

@login_required
def requests_view(request):
    user = request.user
    profile = user.facilityprofile
    requests = profile.requests.all()
    donations = profile.donations.all()

    total_requests = requests.count()
    approved_requests_count = requests.filter(
        approval_status='approved').count()
    rejected_requests_count = requests.filter(
        approval_status='rejected').count()
    pending_requests_count = requests.filter(
        approval_status='pending').count()
    

    context = {
        'requests': requests,
        'total_requests': total_requests,
        'approved_requests_count': approved_requests_count,
        'rejected_requests_count': rejected_requests_count,
        'pending_requests_count': pending_requests_count,
        'profile': profile,
        'user': user
    }

    return render(request, "facility/blood-requests.html", context)


@login_required
def approve_request(request, id):
    request = get_object_or_404(Request, id=id)

    request.approval_status = 'approved'
    request.save()

    return redirect('facility-requests')


@login_required
def reject_request(request, id):
    request = get_object_or_404(Request, id=id)

    request.approval_status = 'rejected'
    request.save()

    return redirect('facility-requests')


# ! DONATIONS

@login_required
def donations_view(request):
    user = request.user
    profile = user.facilityprofile
    donations = profile.donations.all()

    total_donations = donations.count()

    completed_donations = donations.filter(
        status='completed',
    )

    total_blood_donated = sum(
        donation.amount for donation in completed_donations)

    context = {
        'donations': donations,
        'total_donations': total_donations,
        'completed_donations_count': completed_donations.count(),
        'total_blood_donated': total_blood_donated/1000,
        'profile': profile,
        'user': user
    }

    return render(request, "facility/facility-donations.html", context)


@login_required
def approve_donation(request, id):
    donation = get_object_or_404(Donation, id=id)
    donation.approval_status = 'approved'
    donation.save()

    return redirect('facility-donations')


@login_required
def reject_donation(request, id):
    donation = get_object_or_404(Donation, id=id)
    donation.approval_status = 'rejected'
    donation.save()

    return redirect('facility-donations')


@login_required
def mark_donation_complete(request, id):
    donation = get_object_or_404(Donation, id=id)
    donation.status = 'completed'
    donation.save()

    return redirect('facility-donations')
