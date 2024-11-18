
from .models import Donation
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
