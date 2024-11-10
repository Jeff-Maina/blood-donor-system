from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone
from datetime import timedelta


# Create your models here.
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
    eligible = models.BooleanField()
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eligibility Check for {self.user.email} on {self.created_at.date()}"

    def check_eligibility(self):
        min_donation_interval = timedelta(days=90)
        current_date = timezone.now().date()

        if self.last_donation_date and (current_date - self.last_donation_date) < min_donation_interval:
            self.remarks = "Last donation was too recent."
            self.eligible = False
            self.save()
            return self.eligible

        if self.weight < 50:
            self.remarks = "Weight is below the required minimum of 50 kg."
            self.eligible = False
            self.save()
            return self.eligible

        if self.pregnancy_status == "pregnant" or self.is_breastfeeding:
            self.remarks = "Pregnant or breastfeeding individuals cannot donate."
            self.eligible = False
            self.save()
            return self.eligible

        if self.recent_illness or self.recent_travel or self.on_medication or self.chronic_condition:
            self.remarks = "Recent illness, travel, medication use, or chronic condition detected."
            self.eligible = False
            self.save()
            return self.eligible

        if not self.is_in_good_health:
            self.remarks = "User is not in good health."
            self.eligible = False
            self.save()
            return self.eligible

        self.remarks = "User meets all criteria for donation."
        self.eligible = True
        self.save()
        return self.eligible
