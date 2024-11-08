from django import forms
from .models import CustomUser, UserProfile


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


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


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
