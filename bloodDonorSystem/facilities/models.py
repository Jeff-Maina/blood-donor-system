from django.db import models
from users.models import CustomUser

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
    facility = models.ForeignKey(FacilityProfile, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('facility', 'blood_type')