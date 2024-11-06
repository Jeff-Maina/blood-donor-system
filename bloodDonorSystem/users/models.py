from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    profile_completed = models.BooleanField(default=False)
    role = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    county = models.CharField(max_length=100)
    address = models.TextField()
    blood_group = models.CharField(max_length=3)
    gender = models.CharField(max_length=50)
    weight = models.FloatField()
    hemoglobin_level = models.FloatField()
    is_in_good_health = models.BooleanField(default=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)

    def age(self):
        return (timezone.now().date() - self.date_of_birth).days // 365
