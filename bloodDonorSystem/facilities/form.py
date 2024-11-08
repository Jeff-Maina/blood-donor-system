from django import forms
from .models import FacilityProfile
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


class RegisterFacilityForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['facility_name',
                  'email',
                  'registration_number']

        widgets = {
            "facility_name":  forms.TextInput(attrs={'placeholder': 'Full name'}),
            "email": forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            "registration_number":  forms.TextInput(attrs={'placeholder': 'Registration number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileFacilityForm(forms.ModelForm):
    class Meta:
        model = FacilityProfile
        fields = ['name',
                  'contact_number',
                  'facility_type',
                  'county',
                  'open_days',
                  'opening_time',
                  'closing_time',
                  'registration_number']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter the name of the facility'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter the contact name of the facility'}),
            'facility_type': forms.Select(choices=FACILITY_TYPES),
            'county': forms.TextInput(attrs={'placeholder': 'Enter the county of the facility'}),
            'open_days': forms.Select(choices=DAY_CHOICES),
            'opening_time': forms.TimeInput(format='%I:%M %p'),
            'closing_time': forms.TimeInput(format='%I:%M %p'),
            'registration_number': forms.TextInput(attrs={'placeholder': 'Enter the registration of the facility'}),
        }

    def complete_profile(self):
        if self.is_valid:
            profile = self.save()

            return profile
