from django import forms
from .models import CustomUser, UserProfile


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password"}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder" : "Confirm Password"}), label="Confirm Password")

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
        fields = ['county']
