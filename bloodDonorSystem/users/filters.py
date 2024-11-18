
from .models import Donation
from django_filters import FilterSet

class DonationFilter(FilterSet):
    class Meta:
        model = Donation
        fields = ['facility', 'donation_type']
