from django.db import models
from users.models import CustomUser, UserProfile
from datetime import timedelta, datetime

# Create your models here.
FACILITY_TYPES = [
    ('hospital', 'Hospital'),
    ('clinic', 'Clinic'),
    ('community_center', 'Community Center'),
]

DAY_CHOICES = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

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


class FacilityProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    county = models.CharField(max_length=50)
    open_days = models.CharField(max_length=100)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    registration_number = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def operating_hours(self):
        return f"{self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"

    def __str__(self) -> str:
        return f"{self.name}, {self.county} county"


class Inventory(models.Model):
    facility = models.ForeignKey(
        FacilityProfile, on_delete=models.CASCADE, related_name='inventory')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    units_received = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('facility', 'blood_type')

    def __str__(self) -> str:
        return super().__str__()


UNIT_STATUS_CHOICES = [
    ('available', 'Available'),
    ('issued', 'Issued'),
    ('quarantined', 'Quarantined'),
    ('expired', 'Expired'),
]


DONATION_TYPE_CHOICES = [
    ('whole blood', 'Whole Blood Donation'),
    ('plasma', 'Plasma Donation'),
    ('platelets', 'Platelet Donation'),
    ("double red cells", "Double Red Cell Donation"),
]


class BloodUnit(models.Model):
    unit_id = models.CharField(max_length=50, unique=True)
    facility = models.ForeignKey(
        FacilityProfile, on_delete=models.CASCADE, related_name='bloodunits')
    donor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='bloodunits')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    donation_type = models.CharField(max_length=50,choices=DONATION_TYPE_CHOICES)
    collection_date = models.DateField()
    expiration_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=UNIT_STATUS_CHOICES, default='available')
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Unit {self.unit_id} - {self.blood_type} ({self.donation_type})"

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            if self.donation_type == 'whole blood':
                self.expiration_date = self.collection_date + \
                    timedelta(days=42)
            elif self.donation_type == 'plasma':
                self.expiration_date = self.collection_date + \
                    timedelta(days=365)
            elif self.donation_type == 'platelets':
                self.expiration_date = self.collection_date + timedelta(days=7)
            elif self.donation_type == 'double red cells':
                self.expiration_date = self.collection_date + \
                    timedelta(days=42)
        super().save(*args, **kwargs)
