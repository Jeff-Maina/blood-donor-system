from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone
from datetime import timedelta, datetime
import hashlib
import string
import random
# Create your models here.


def generate_hash(*args):
    return hashlib.sha256("".join(map(str, args)).encode()).hexdigest()[:10].upper()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    profile_completed = models.BooleanField(default=False)
    role = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50, null=True)
    facility_name = models.CharField(max_length=100, null=True)
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user_uuid = models.CharField(max_length=50, unique=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=15, null=True)
    lastname = models.CharField(max_length=15, null=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    county = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    gender = models.CharField(max_length=50)

    def age(self):
        today = timezone.now().date()
        return (today - self.date_of_birth).days // 365

    @property
    def age_display(self):
        return self.age()

    def save(self, *args, **kwargs):
        if not self.user_uuid:
            initials = f"{self.firstname[0].upper()}{self.lastname[0].upper()}"
            random_code = ''.join(random.choices(string.digits, k=5))
            self.user_uuid = f"DNR-{initials}-{random_code}"
        super().save(*args, **kwargs)


class DonationEligibity(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_donation_date = models.DateField(null=True, blank=True)
    weight = models.IntegerField(default=False)
    pregnancy_status = models.CharField(max_length=50)
    recent_illness = models.BooleanField(default=False)
    recent_travel = models.BooleanField(default=False)
    on_medication = models.BooleanField(default=False)
    is_in_good_health = models.BooleanField(default=False)
    is_breastfeeding = models.BooleanField(default=False)
    chronic_condition = models.BooleanField(default=False)
    eligible = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eligibility Check for {self.user.email} on {self.created_at.date()}"

    def check_eligibility(self):
        min_donation_interval = timedelta(days=90)
        current_date = timezone.now().date()
        reasons = []

        if self.last_donation_date and (current_date - self.last_donation_date) < min_donation_interval:
            reasons.append("Last donation was too recent.")

        if self.weight < 50:
            reasons.append("Weight is below the required minimum of 50 kg.")

        if self.pregnancy_status == "pregnant" or self.is_breastfeeding:
            reasons.append(
                "Pregnant or breastfeeding individuals cannot donate.")

        if self.recent_illness or self.recent_travel or self.on_medication or self.chronic_condition:
            reasons.append(
                "Recent illness, travel, medication use, or chronic condition detected.")

        if not self.is_in_good_health:
            reasons.append("You are not in good health.")

        self.remarks = "User meets all criteria for donation." if self.eligible else "User does not meet all criteria"
        self.eligible = len(reasons) == 0

        self.save()

        return self.eligible, reasons


class Donation(models.Model):
    from facilities.models import FacilityProfile

    DONATION_TYPE_CHOICES = [
        ('whole blood', 'Whole Blood Donation'),
        ('plasma', 'Plasma Donation'),
        ('platelets', 'Platelet Donation'),
        ("double red cells", "Double Red Cell Donation"),
    ]

    DONATION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    donation_id = models.CharField(max_length=50, unique=True, null=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='donations')
    facility = models.ForeignKey(
        FacilityProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')

    amount = models.DecimalField(max_digits=5, decimal_places=2)
    donation_type = models.CharField(
        max_length=50, choices=DONATION_TYPE_CHOICES)
    donation_date = models.DateTimeField()
    status = models.CharField(
        max_length=50, default='scheduled', choices=DONATION_STATUS_CHOICES)
    approval_status = models.CharField(
        default="pending", max_length=50, choices=APPROVAL_STATUS_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True, default='')
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation for {self.user} on {self.created_at.date()} with status {self.status}"

    def save(self, *args, **kwargs):
        if not self.donation_id:
            unique_str = f"{self.user.id}-{self.facility.id if self.facility else 'NA'}-{self.donation_type}-{datetime.now()}"
            self.donation_id = f"DON-{generate_hash(unique_str)}"
        super().save(*args, **kwargs)


class Request(models.Model):
    from facilities.models import FacilityProfile

    DONATION_TYPE_CHOICES = [
        ('whole blood', 'Whole Blood Donation'),
        ('plasma', 'Plasma Donation'),
        ('platelets', 'Platelet Donation'),
        ("double red cells", "Double Red Cell Donation"),
    ]

    URGENCY_LEVEL_CHOICES = [
        ('normal', 'normal'),
        ('urgent', 'urgent'),
        ('critical', 'critical'),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    REQUEST_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    request_id = models.CharField(max_length=50, unique=True, null=True)

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='requests')
    facility = models.ForeignKey(
        FacilityProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')

    request_type = models.CharField(
        max_length=50, choices=DONATION_TYPE_CHOICES)

    needed_by = models.DateTimeField()
    request_amount = models.DecimalField(max_digits=5, decimal_places=2)
    approval_status = models.CharField(
        max_length=50, default='pending', choices=APPROVAL_STATUS_CHOICES)
    request_status = models.CharField(
        max_length=50, default='scheduled', choices=REQUEST_STATUS_CHOICES)
    rejection_reason = models.TextField(blank=True, null=True)
    urgency_level = models.CharField(
        max_length=50, choices=URGENCY_LEVEL_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.user} on {self.created_at.date()} ({self.request_amount} ml)"

    def save(self, *args, **kwargs):
        if not self.request_id:
            unique_str = f"{self.user.id}-{self.facility.id if self.facility else 'NA'}-{self.request_type}-{datetime.now()}"
            self.request_id = f"REQ-{generate_hash(unique_str)}"
        super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    doer = models.CharField(max_length=60, null=True)
    action = models.CharField(max_length=50, default="", null=True)
    type = models.CharField(max_length=50, default="", null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message}"
