
from .models import Donation, Request
from django_filters import FilterSet
from django_filters import DateFilter
from django import forms


class DonationFilter(FilterSet):

    start_date = DateFilter(
        field_name='donation_date',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label='Start Date'
    )

    end_date = DateFilter(
        field_name='donation_date',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label='End Date'
    )

    class Meta:
        model = Donation
        fields = ['facility', 'donation_type', 'status',
                  'approval_status', 'start_date', 'end_date']


class RequestsFilter(FilterSet):

    start_date = DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gte',
        label='Start Date'
    )

    end_date = DateFilter(
        field_name='created_at',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='lte',
        label='End Date'
    )

    class Meta:
        model = Request
        fields = ['facility', 'request_type', 'request_status',
                  'urgency_level', 'approval_status']
