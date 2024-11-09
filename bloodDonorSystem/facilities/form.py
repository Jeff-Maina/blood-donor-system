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
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
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
    open_days = forms.MultipleChoiceField(
        choices=DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select all days the facility is open."
    )

    class Meta:
        model = FacilityProfile
        fields = [
                  'facility_type',
                  'contact_number',
                  'county',
                  'open_days',
                  'opening_time',
                  'closing_time']

        widgets = {
            'facility_type': forms.Select(choices=FACILITY_TYPES),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter the contact name of the facility'}),
            'county': forms.TextInput(attrs={'placeholder': 'Enter the county of the facility'}),
            'opening_time': forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
            'closing_time': forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
        }

        help_texts = {
            'opening_time': 'Enter opening time in HH:MM 24-hour format.',
            'closing_time': 'Enter closing time in HH:MM 24-hour format.',
        }

    def complete_profile(self):
        if self.is_valid():
            profile = self.save(commit=False)
            profile.user = self.instance.user
            profile.open_days = ','.join(self.cleaned_data['open_days'])
            profile.save()
            self.instance.user.profile_completed = True
            self.instance.user.save()
            return profile
