from django import forms
from .models import CustomUser, UserProfile, DonationEligibity, Donation
from django.core.exceptions import ValidationError
from datetime import datetime, time
from django.utils import timezone

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


GENDERS = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
            "email": forms.TextInput(attrs={'placeholder': 'Enter your email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the hashed password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'date_of_birth',
            'phone',
            'firstname',
            'lastname',
            'county',
            'blood_group',
            'gender',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'Enter your firstname'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Enter your lastname'}),
            'county': forms.TextInput(attrs={'placeholder': 'Enter your county'}),
            'blood_group': forms.Select(choices=BLOOD_TYPES, attrs={"class": "custom-select"}),
            'gender': forms.Select(choices=GENDERS),
        }

    def complete_profile(self):
        if self.is_valid:
            profile = self.save()

            return profile


class EligibilityForm(forms.ModelForm):
    BOOLEAN_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]

    pregnancy_status = forms.ChoiceField(
        label='Are you currently pregnant?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    recent_illness = forms.ChoiceField(
        label='Have you had a recent illness?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    recent_travel = forms.ChoiceField(
        label='Have you traveled outside the country in the last 6 months?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    on_medication = forms.ChoiceField(
        label='Are you currently on any medication?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    is_in_good_health = forms.ChoiceField(
        label='Are you in good health today?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    is_breastfeeding = forms.ChoiceField(
        label='Are you currently breastfeeding?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    chronic_condition = forms.ChoiceField(
        label='Do you have any chronic medical conditions?',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )

    last_donation_date = forms.DateField(
        label='When was your last blood donation?',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = DonationEligibity
        fields = [
            'weight',
            'last_donation_date',
            'pregnancy_status',
            'recent_illness',
            'recent_travel',
            'on_medication',
            'is_in_good_health',
            'is_breastfeeding',
            'chronic_condition'
        ]

        labels = {
            'weight': 'Enter your current weight (Kgs)',
        }


class BookDonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ['amount', 'donation_type',
                  'donation_date', 'remarks']

        widgets = {
            'amount': forms.NumberInput(attrs={'min': '100', 'max': '800', 'step': '1'}),
            'donation_type': forms.Select(attrs={'class': 'form-control'}),
            'donation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Any additional information? e.g special considerations, preferred staff.'}),
        }

        labels = {
            'donation_date' : "Appointment Date and Time",
        }

    def clean_donation_date(self):
        donation_date = self.cleaned_data.get('donation_date')

        if donation_date and timezone.is_naive(donation_date):
            donation_date = timezone.make_aware(
                donation_date, timezone.get_current_timezone())

        if donation_date <= timezone.now():
            raise ValidationError("The donation date must be in the future.")

        if not (time(9, 0) <= donation_date.time() <= time(18, 0)):
            raise ValidationError(
                "The donation time must be between 9:00 AM and 6:00 PM.")

        return donation_date
