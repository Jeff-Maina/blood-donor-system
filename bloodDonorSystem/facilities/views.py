from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import RegisterFacilityForm, ProfileFacilityForm
from users.models import CustomUser, Request, Donation, UserProfile, Notification
from .models import FacilityProfile, Inventory, BloodUnit
from django.contrib.auth import authenticate, login, logout
from .decorators import facility_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum, Count
from datetime import datetime
from .tables import FacilityDonationsTable, FaciltyRequestsTable, InventoryTable, BloodUnitsTable, DonorsTable
from .filters import FacilityDonationsFilter, FacilityRequestsFilter, InventoryFilter, BloodUnitsFilter, DonorsFilter
from django_tables2 import RequestConfig

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
                    'total_blood_donated': total_blood_donated/1000,

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


@login_required
def profile_settings_view(request):
    user = request.user
    profile = FacilityProfile.objects.filter(user=user).first()

    if request.method == 'POST':
        form = ProfileFacilityForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("facility-profile-settings")
    else:
        form = ProfileFacilityForm(instance=profile)
    return render(request, "facility/profile-settings.html", {"form": form, 'user': user, 'profile': profile})

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

    if 'clear_facility_requests_filters' in request.GET:
        request.GET = request.GET.copy()
        request.GET.clear()

    facility_requests_filter = FacilityRequestsFilter(
        request.GET, queryset=requests)
    filtered_requests = facility_requests_filter.qs

    facility_requests_table = FaciltyRequestsTable(filtered_requests)
    RequestConfig(request).configure(facility_requests_table)

    context = {
        'requests': requests,
        'total_requests': total_requests,
        'approved_requests_count': approved_requests_count,
        'rejected_requests_count': rejected_requests_count,
        'pending_requests_count': pending_requests_count,
        'profile': profile,
        'user': user,
        'facility_requests_table': facility_requests_table,
        'facility_requests_filter': facility_requests_filter
    }

    return render(request, "facility/requests/blood-requests.html", context)


@login_required
def approve_request(request, id):
    request = get_object_or_404(Request, id=id)

    notification = Notification.objects.create(
        doer=f'{request.facility.name}',
        action=f'approved your request for <span style="color: black; font-weight: 600">{request.request_amount} ml , {request.request_type}</span>',
        user=request.user.user,
        type='request-approval'
    )

    request.approval_status = 'approved'
    request.save()
    notification.save()

    return redirect('facility-requests')


@login_required
def reject_request(request, id):
    user_request = get_object_or_404(Request, id=id)

    if request.method == 'POST':
        rejection_reason = request.POST.get('reason')
        user_request.approval_status = 'rejected'
        user_request.rejection_reason = rejection_reason

        notification = Notification.objects.create(
            doer=f'{user_request.facility.name}',
            action=f'rejected your request for <span style="color: black; font-weight: 600">{user_request.request_amount} ml , {user_request.request_type}</span> due to <span style="color: black; font-weight: 600">{user_request.rejection_reason}</span>',
            user=user_request.user.user,
            type='request-rejection'
        )

        user_request.save()
        notification.save()
        return redirect('facility-requests')

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

    # table logic
    if 'clear_facility_donations_filters' in request.GET:
        request.GET = request.GET.copy()
        request.GET.clear()

    facility_donations_filter = FacilityDonationsFilter(
        request.GET, queryset=donations)

    filtered_donations = facility_donations_filter.qs
    facility_donations_table = FacilityDonationsTable(filtered_donations)

    RequestConfig(request).configure(facility_donations_table)

    context = {
        'donations': donations,
        'total_donations': total_donations,
        'completed_donations_count': completed_donations.count(),
        'total_blood_donated': total_blood_donated/1000,
        'profile': profile,
        'user': user,
        'facility_donations_filter': facility_donations_filter,
        'facility_donations_table': facility_donations_table
    }

    return render(request, "facility/donations/facility-donations.html", context)


@login_required
def approve_donation(request, id):
    donation = get_object_or_404(Donation, id=id)
    donation.approval_status = 'approved'

    notification = Notification.objects.create(
        doer=f'{donation.facility.name}',
        action=f'approved your appointment for <span style="color: black; font-weight: 600">{donation.donation_type}</span> donation on <span style="color: black; font-weight: 600">{donation.donation_date.date()}</span>',
        user=donation.user.user,
        type='appointment-approval'
    )

    donation.save()
    notification.save()

    return redirect('facility-donations')


@login_required
def reject_donation(request, id):
    donation = get_object_or_404(Donation, id=id)

    if request.method == 'POST':
        rejection_reason = request.POST.get('reason')
        donation.approval_status = 'rejected'
        donation.rejection_reason = rejection_reason

        notification = Notification.objects.create(
            doer=f'{donation.facility.name}',
            action=f'rejected your appointment for <span style="color: black; font-weight: 600">{donation.donation_type}</span> on <span style="color: black; font-weight: 600">{donation.donation_date.date()}</span> due to <span style="color: black; font-weight: 600">{donation.rejection_reason}</span>',
            user=donation.user.user,
            type='appointment-rejection'
        )

        donation.save()
        notification.save()

        return redirect('facility-donations')

    return redirect('facility-donations')


@login_required
def mark_donation_complete(request, id):
    donation = get_object_or_404(Donation, id=id)

    blood_unit = BloodUnit.objects.create(
        blood_type=donation.user.blood_group,
        donation_type=donation.donation_type,
        quantity=donation.amount,
        donor=donation.user,
        facility=donation.facility,
        collection_date=donation.donation_date,
        status='available',
    )

    notification = Notification.objects.create(
        doer=f'{donation.facility.name}',
        action=f'confirmed completion of your <span style="color: black; font-weight: 600">{donation.donation_type}</span> donation on <span style="color: black; font-weight: 600">{donation.donation_date.date()}</span>',
        user=donation.user.user,
        type='donation-completion'
    )

    donation.status = 'completed'
    donation.save()
    notification.save()

    blood_unit.save()

    return redirect('facility-donations')


# ! INVENTORY
@login_required
def inventory_view(request):
    user = request.user
    profile = user.facilityprofile

    inventory = profile.inventory.all()

    bloodunits = profile.bloodunits.all()

    available_blood_units = profile.bloodunits.filter(status='available').values('blood_type').annotate(
        available_units=Count('unit_id')
    )

    available_units_map = {
        unit['blood_type']: unit['available_units'] for unit in available_blood_units}

    for item in inventory:
        item.quantity = round(item.quantity / 1000, 3)

    def get_restock_label(quantity):
        if quantity < 1.0:
            return "Critical"
        elif 1.0 <= quantity < 3.0:
            return "Low"
        elif 3.0 <= quantity < 5.0:
            return "Adequate"
        else:
            return "Surplus"

    # tables

    facility_inventory_filter = InventoryFilter(
        request.GET, queryset=inventory, prefix='inventory')
    filtered_inventory = facility_inventory_filter.qs

    filtered_inventory_data = [
        {
            "blood_type": item.blood_type,
            "total_quantity": round(item.quantity / 1000, 3),
            "units_received": item.units_received,
            "updated_at": item.updated_at,
            "restock_status": get_restock_label(round(item.quantity / 1000, 3)),
            "available_units": available_units_map.get(item.blood_type, 0),
        }
        for item in filtered_inventory
    ]

    inventory_table = InventoryTable(filtered_inventory_data, prefix="1-")

    # bloodunits table

    bloodunits_filter = BloodUnitsFilter(
        request.GET, queryset=bloodunits, prefix='bloodunit')
    filtered_bloodunits = bloodunits_filter.qs

    bloodunits_table = BloodUnitsTable(filtered_bloodunits, prefix='2-')

    RequestConfig(request).configure(inventory_table)
    RequestConfig(request).configure(bloodunits_table)

    context = {
        'inventories': filtered_inventory_data,
        'profile': profile,
        'user': user,
        'bloodunits_filter': bloodunits_filter,
        'bloodunits_table': bloodunits_table,
        'facility_inventory_filter': facility_inventory_filter,
        'inventory_table': inventory_table
    }

    return render(request, 'facility/inventory/inventory.html', context)


@receiver(post_save, sender=Donation)
def update_inventory_on_completion(sender, instance, **kwargs):
    if instance.status == 'completed':
        facility = instance.facility
        blood_type = instance.user.blood_group
        amount = Decimal(instance.amount)

        inventory, created = Inventory.objects.get_or_create(
            facility=facility,
            blood_type=blood_type,
            defaults={'quantity': Decimal(0)})

        inventory.quantity += amount
        inventory.units_received += 1
        inventory.save()


# ! DONOR MANAGEMENT

@login_required
def donor_management_view(request):
    profile = request.user.facilityprofile
    donations = Donation.objects.filter(facility=profile)
    user_profiles = UserProfile.objects.filter(
        id__in=donations.values_list('user', flat=True).distinct())

    donors_info = []

    donors_filter = DonorsFilter(request.GET, queryset=user_profiles)
    filtered_donors = donors_filter.qs

    for user_profile in filtered_donors:
        user_requests = Request.objects.filter(
            user=user_profile, facility=profile)

        profile_info = {
            'profile': user_profile,
            'donations': donations.filter(user=user_profile),
            'total_donations': donations.filter(user=user_profile).count(),
            'completed_donations': donations.filter(user=user_profile, status='completed').count(),
            'total_blood_donated': sum(donation.amount for donation in donations.filter(user=user_profile, status='completed'))/1000,
            'total_requests': user_requests.count(),
            'pending_requests': user_requests.filter(approval_status='pending').count(),
            'approved_requests': user_requests.filter(approval_status='approved').count(),
            'rejected_requests': user_requests.filter(approval_status='rejected').count()
        }

        donors_info.append(profile_info)

    donors_table = DonorsTable(donors_info)
    RequestConfig(request).configure(donors_table)

    context = {
        'total_donors': len(donors_info),
        'male_donors_count': user_profiles.filter(gender='Male').count(),
        'female_donors_count': user_profiles.filter(gender='Female').count(),
        'profile': profile,
        'user': request.user,
        'donors_table': donors_table,
        'donors_filter': donors_filter
    }

    return render(request, 'facility/donors/donor-management.html', context)


@login_required
def donor_view(request, user_uuid):
    user = request.user
    facility_profile = user.facilityprofile
    donor_profile = get_object_or_404(UserProfile, user_uuid=user_uuid)
    donor_requests = donor_profile.requests.all().filter(facility=facility_profile)
    donor_donations = donor_profile.donations.all().filter(facility=facility_profile)

    pending_requests = donor_requests.filter(approval_status='pending').count()
    rejected_requests = donor_requests.filter(approval_status='rejected').count()
    approved_requests = donor_requests.filter(approval_status='approved').count()

    completed_donations = donor_donations.filter(status='completed').count()
    pending_donations = donor_donations.filter(status='scheduled').count()
    cancelled_donations = donor_donations.filter(status='cancelled').count()

    context = {
        'donor_profile': donor_profile,
        'user': user,
        'profile': facility_profile,
        'total_requests': donor_requests.count(),
        'total_donations': donor_donations.count(),
        'pending_requests': pending_requests,
        'rejected_requests': rejected_requests,
        'approved_requests': approved_requests,
        'completed_donations': completed_donations,
        'pending_donations': pending_donations,
        'cancelled_donations': cancelled_donations
    }

    return render(request, "facility/donors/donor-details.html", context)
