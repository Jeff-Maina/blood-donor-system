import django_filters
from users.models import Donation
from django import forms


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
        fields = [ 'donation_type', 'status', 'approval_status']
