from django.shortcuts import render, redirect, get_object_or_404
from .form import RegisterUserForm, UserProfileForm, EligibilityForm, BookDonationForm, RequestBloodForm
from .models import CustomUser, UserProfile, DonationEligibity, Donation, Request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
# Create your views here.


def home_view(request):
    return render(request, 'home.html')


def get_started(request):
    return render(request, 'get-started.html')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = CustomUser.objects.create_user(
                email=email, password=password, role='individual'
            )

            login(request, user)
            return redirect("complete-profile")
    else:
        form = RegisterUserForm()
    return render(request, "user/register.html", {'form': form})


def login_user(request):
    error_message = None

    if request.user.is_authenticated:
        if request.user.role == 'individual':
            return redirect("user-dashboard")
        else:
            if request.user.is_approved:
                return redirect('facility-dashboard')
            else:
                return redirect("awaiting-approval")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email,
                            password=password, is_approved=True)

        if user is not None:
            login(request, user)

            if user.role == 'individual':
                if user.profile_completed:
                    return redirect("user-dashboard")
                else:
                    return redirect("complete-profile")
            else:
                return redirect("facility-dashboard")

        else:
            if CustomUser.objects.filter(email=email).exists():
                print(f"{email,password}")
                error_message = "Incorrect credentials. Please try again."
            else:
                error_message = "No account found with that email. Please register."

    return render(request, 'login.html', {'error': error_message})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("login")
    else:
        return redirect("home")


@login_required
def complete_profile(request):

    if request.user.profile_completed:
        return redirect("user-dashboard")

    if request.method == "POST":

        form = UserProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user.profile_completed = True
            request.user.save()
            profile.save()
            return redirect("user-dashboard")
    else:
        form = UserProfileForm()
    return render(request, "user/complete-profile.html", {"form": form})


@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin index page

    profile = UserProfile.objects.filter(user=user).first()
    donations = profile.donations.all()
    total_donations = donations.count()
    upcoming_donations = donations.filter(
        status='scheduled',
        approval_status='pending',
        donation_date__gte=datetime.now()
    ).order_by('donation_date')

    if user.role == 'individual':
        context = {
            'user': user,
            'profile': profile,
            'upcoming_donations': upcoming_donations,
            'total_donations': total_donations
        }
        return render(request, 'user/dashboard.html', context)
    else:
        return redirect(request, 'facility-dashboard')


@login_required
def donations_view(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    donations = profile.donations.all()
    total_donations = donations.count()
    last_donation = donations.filter(
        status='completed').order_by('donation_date').last()

    if last_donation:
        last_donation_date = last_donation.donation_date.strftime(
            "%B %d, %Y at  %I:%M %p")
    else:
        last_donation_date = '-'

    if user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin index page

    if user.role == 'individual':
        return render(request, 'user/donations.html', {'user': user, 'profile': profile, 'donations': donations, 'total_donations': total_donations, "last_donation_date": last_donation_date})
    else:
        return redirect(request, 'facility-dashboard')


@login_required
def requests_view(request):
    user = request.user

    if user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin index page

    profile = UserProfile.objects.filter(user=user).first()
    requests = profile.requests.all()
    approved_requests_count = requests.filter(
        approval_status='approved').count()
    rejected_requests_count = requests.filter(
        approval_status='rejected').count()
    total_requests = requests.count()

    if user.role == 'individual':
        context = {
            'user': user,
            'profile': profile,
            'requests': requests,
            'approved_requests_count': approved_requests_count,
            'rejected_requests_count': rejected_requests_count,
            'total_requests': total_requests
        }
        return render(request, 'user/requests.html', context)
    else:
        return redirect(request, 'facility-dashboard')


@login_required
def check_eligibility(request):

    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    donations = profile.donations.all()
    total_donations = donations.count()

    try:
        eligibility_record = DonationEligibity.objects.get(user=request.user)
    except DonationEligibity.DoesNotExist:
        eligibility_record = None

    is_eligible = None
    reasons = []

    if request.method == 'POST':
        form = EligibilityForm(request.POST, instance=eligibility_record)

        if form.is_valid():
            eligibility = form.save(commit=False)
            eligibility.user = request.user
            eligibility.save()

            is_eligible, reasons = eligibility.check_eligibility()

            if is_eligible:
                return redirect('book-donation-appointment')
            else:
                return render(request, 'user/not-eligible.html', {'reasons': reasons, 'donations': donations, 'total_donations': total_donations})
    else:
        form = EligibilityForm(instance=eligibility_record)

    return render(request, 'user/eligibility-form.html', {
        'form': form,
        'profile': profile,
        'is_eligible': is_eligible,
        'reasons': reasons,
        'donations': donations, 'total_donations': total_donations
    })


@login_required
def book_appointment(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    donations = profile.donations.all()
    total_donations = donations.count()

    try:
        eligibility = DonationEligibity.objects.get(user=user)
    except DonationEligibity.DoesNotExist:
        return redirect('check-eligibility')

    if not eligibility.eligible:
        return redirect('check-eligibility')

    if request.method == 'POST':
        form = BookDonationForm(request.POST)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = profile
            donation.save()

            return redirect('donations')
        else:
            return render(request, 'user/book-donation.html', {'form': form, 'donations': donations, 'total_donations': total_donations})
    else:
        form = BookDonationForm()
    return render(request, 'user/book-donation.html', {'form': form, 'donations': donations, 'total_donations': total_donations})


@login_required
def deleteDonation(request, id):

    donation = get_object_or_404(Donation, id=id)
    profile = UserProfile.objects.filter(user=request.user).first()
    if donation.user != profile:
        return redirect("home")
    donation.delete()
    return redirect("donations")


@login_required
def updateDonation(request, id):
    donation = get_object_or_404(Donation, id=id)
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    if donation.user != profile:
        return redirect("home")

    if request.method == "POST":
        form = BookDonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect("donations")
    else:
        form = BookDonationForm(instance=donation)
    return render(request, "user/update-donation.html", {"form": form, 'user': user, 'profile': profile, })


@login_required
def cancel_appointment(request, id):
    donation = get_object_or_404(Donation, id=id)
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    if donation.user != request.user:
        return redirect("home")

    donation.status = 'cancelled'
    donation.save()

    return redirect('donations')


@login_required
def make_request(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    requests = profile.requests.all()
    approved_requests_count = requests.filter(
        approval_status='approved').count()
    rejected_requests_count = requests.filter(
        approval_status='rejected').count()
    total_requests = requests.count()

    if request.method == 'POST':
        form = RequestBloodForm(request.POST)

        if form.is_valid():
            request = form.save(commit=False)
            request.user = profile
            request.save()
            return redirect('requests')
        else:

            return render(request, 'user/make-request.html',
                          {'form': form, 'user': user, 'profile': profile, 'requests': requests, 'approved_requests_count': approved_requests_count, 'rejected_requests_count': rejected_requests_count, 'total_requests': total_requests})
    else:
        form = RequestBloodForm()
    return render(request, 'user/make-request.html', {'form': form, 'user': user, 'profile': profile, 'requests': requests, 'approved_requests_count': approved_requests_count, 'rejected_requests_count': rejected_requests_count, 'total_requests': total_requests})


@login_required
def deleteRequest(request, id):
    request = get_object_or_404(Request, id=id)

    request.delete()
    return redirect("requests")

@login_required
def cancel_request(request, id):
    request = get_object_or_404(Request, id=id)
 
    request.request_status = 'cancelled'
    request.save()

    return redirect('requests')
