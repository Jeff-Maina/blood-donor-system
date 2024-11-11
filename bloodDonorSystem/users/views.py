from django.shortcuts import render, redirect
from .form import RegisterUserForm, UserProfileForm, EligibilityForm, BookDonationForm
from .models import CustomUser, UserProfile, DonationEligibity
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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

    profile = UserProfile.objects.filter(user=user).first()

    if user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin index page

    if user.role == 'individual':
        return render(request, 'user/dashboard.html', {'user': user, 'profile': profile})
    else:
        return redirect(request, 'facility-dashboard')


@login_required
def donations_view(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    donations = user.donations.all()
    total_donations = donations.count()
    last_donation = donations.filter(status='completed').order_by('donation_date').last()

    if  last_donation:
        last_donation_date = last_donation.donation_date.strftime("%B %d, %Y at  %I:%M %p")
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
    profile = UserProfile.objects.filter(user=user).first()

    if user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin index page

    if user.role == 'individual':
        return render(request, 'user/requests.html', {'user': user, 'profile': profile})
    else:
        return redirect(request, 'facility-dashboard')


@login_required
def check_eligibility(request):

    user = request.user
    profile = UserProfile.objects.filter(user=user).first()

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
                return render(request, 'user/not-eligible.html', {'reasons': reasons})
    else:
        form = EligibilityForm(instance=eligibility_record)

    return render(request, 'user/eligibility-form.html', {
        'form': form,
        'profile': profile,
        'is_eligible': is_eligible,
        'reasons': reasons,
    })


@login_required
def book_appointment(request):
    user = request.user

    try:
        eligibility = DonationEligibity.objects.get(user=user)
    except DonationEligibity.DoesNotExist:
        return redirect('check-eligibility')

    if not eligibility.eligible:
        return redirect('check-eligibility')

    if request.method == 'POST':
        form = BookDonationForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            donation = form.save(commit=False)
            donation.user = user
            donation.save()

            return redirect('donations')
        else:
            return render(request, 'user/book-donation.html', {'form': form})
    else:
        form = BookDonationForm()
    return render(request, 'user/book-donation.html', {'form': form})
