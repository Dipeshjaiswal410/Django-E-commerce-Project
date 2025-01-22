from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Corrected this line to use 'Profile'
        fields = ['address', 'phone_number']  # Correct field names based on your models
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
        }