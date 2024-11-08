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
    firstname = models.CharField(max_length=15,null=True)
    lastname = models.CharField(max_length=15,null=True)
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