import django_filters
from users.models import Donation, Request
from django import forms

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

    class Meta:
        model = Donation
        fields = ['donation_type', 'status', 'approval_status']


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
