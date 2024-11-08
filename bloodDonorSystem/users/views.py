from django.shortcuts import render, redirect
from .form import RegisterUserForm, UserProfileForm
from .models import CustomUser, UserProfile
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
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email,
                            password=password, is_approved=True)

        if user is not None:
            login(request, user)

            if user.role == 'individual':
                if user.profile_completed:
                    return redirect("dashboard")
                else:
                    return redirect("complete-profile")
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
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.user.profile_completed:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user.profile_completed = True
            request.user.save()
            profile.save()
            return redirect("dashboard")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "user/complete-profile.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html')
