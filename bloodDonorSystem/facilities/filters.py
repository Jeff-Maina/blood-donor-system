import django_filters
from users.models import Donation, Request, UserProfile
from django import forms
from .models import Inventory, BloodUnit

BLOOD_TYPES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

GENDERS = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class FacilityDonationsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label='Start Date'
    )

    end_date = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label='End Date'
    )

    blood_group = django_filters.ChoiceFilter(
        field_name='user__blood_group',
        choices=BLOOD_TYPES,
        lookup_expr='iexact',
        label='Blood Group'
    )

    class Meta:
        model = Donation
        fields = ['donation_type', 'blood_group', 'status', 'approval_status']


class FacilityRequestsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label='Start Date'
    )

    end_date = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label='End Date'
    )

    blood_group = django_filters.ChoiceFilter(
        field_name='user__blood_group',
        choices=BLOOD_TYPES,
        lookup_expr='iexact',
        label='Blood Group'
    )

    class Meta:
        model = Request
        fields = ['request_type', 'blood_group',
                  'request_status', 'approval_status', 'urgency_level']


class InventoryFilter(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = ['blood_type']


class BloodUnitsFilter(django_filters.FilterSet):
    class Meta:
        model = BloodUnit
        fields = ['blood_type', 'donation_type', 'status']


class DonorsFilter(django_filters.FilterSet):
    blood_group = django_filters.ChoiceFilter(
        field_name='blood_group',
        choices=BLOOD_TYPES,
        lookup_expr='iexact',
        label='Blood Group'
    )

    gender = django_filters.ChoiceFilter(
        field_name='gender',
        choices=GENDERS,
        lookup_expr='iexact',
        label='Gender'
    )

    county = django_filters.CharFilter(
        field_name='county',
        lookup_expr='iexact',
        label='County'
    )

    class Meta:
        model = UserProfile
        fields = ['county', 'blood_group', 'gender']
